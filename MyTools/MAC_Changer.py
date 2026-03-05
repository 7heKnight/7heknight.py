#!/usr/bin/env python3
"""Cross-platform MAC address changer.

Supports Linux, macOS, and Windows. Automatically requests elevated
privileges (root/sudo on Unix, Administrator via UAC on Windows)
when not already running with sufficient permissions.
"""

import argparse
import ctypes
import os
import platform
import re
import shutil
import subprocess
import sys
import time

MAC_PATTERN = re.compile(r"^([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}$")
MAC_EXTRACT = re.compile(
    r"[0-9A-Fa-f]{2}(?:[:\-])[0-9A-Fa-f]{2}(?:[:\-])[0-9A-Fa-f]{2}"
    r"(?:[:\-])[0-9A-Fa-f]{2}(?:[:\-])[0-9A-Fa-f]{2}(?:[:\-])[0-9A-Fa-f]{2}"
)


# ---------------------------------------------------------------------------
# Privilege elevation
# ---------------------------------------------------------------------------

def is_elevated():
    """Return True if the process has administrator/root privileges."""
    if platform.system() == "Windows":
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            return False
    else:
        return os.geteuid() == 0


def _elevate_windows():
    """Re-launch the current script with a UAC elevation prompt."""
    params = " ".join(f'"{a}"' if " " in a else a for a in sys.argv)
    try:
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1  # SW_SHOWNORMAL
        )
        # ShellExecuteW returns >32 on success, <=32 on failure
        if ret <= 32:
            print("[-] UAC elevation was declined or failed.")
            sys.exit(1)
    except (AttributeError, OSError) as exc:
        print(f"[-] Failed to request elevation: {exc}")
        sys.exit(1)
    # The elevated process runs separately; this (unelevated) process exits.
    sys.exit(0)


def _elevate_unix():
    """Re-exec the current script under *sudo*."""
    sudo = shutil.which("sudo")
    if sudo is None:
        print("[-] 'sudo' not found. Please run this script as root.")
        sys.exit(1)
    print("[+] Requesting root privileges via sudo...")
    try:
        os.execvp(sudo, [sudo, sys.executable] + sys.argv)
    except OSError as exc:
        print(f"[-] Failed to re-exec with sudo: {exc}")
        sys.exit(1)


def ensure_elevated():
    """If not already elevated, re-launch with the appropriate mechanism."""
    if is_elevated():
        return
    print("[!] This script requires elevated privileges.")
    if platform.system() == "Windows":
        print("[+] Requesting Administrator privileges via UAC...")
        _elevate_windows()
    else:
        _elevate_unix()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_args(argv=None):
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Cross-platform MAC address changer."
    )
    parser.add_argument(
        "-i", "--interface",
        required=True,
        help="Network interface name to modify.",
    )
    parser.add_argument(
        "-m", "--mac",
        required=True,
        dest="new_mac",
        help="New MAC address (format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX).",
    )
    parser.add_argument(
        "--no-elevate",
        action="store_true",
        default=False,
        help="Skip automatic privilege elevation (useful for testing/CI).",
    )
    return parser.parse_args(argv)


def normalize_mac(mac):
    """Normalize MAC to colon-separated lowercase hex."""
    return mac.replace("-", ":").lower()


def validate_mac(mac):
    """Return a normalized MAC or exit with an error message."""
    if not MAC_PATTERN.match(mac):
        print(f"[-] Invalid MAC address format: {mac}")
        print("    Expected format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX")
        sys.exit(1)
    return normalize_mac(mac)


def run_command(cmd, capture=True):
    """Execute *cmd* and return :class:`subprocess.CompletedProcess`."""
    try:
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        print(f"[-] Command not found: {cmd[0]}")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f'[-] Command timed out: {" ".join(cmd)}')
        sys.exit(1)


# ---------------------------------------------------------------------------
# Linux
# ---------------------------------------------------------------------------

def _has_ip_command():
    return shutil.which("ip") is not None


def get_current_mac_linux(interface):
    """Retrieve the current MAC address on Linux."""
    if _has_ip_command():
        result = run_command(["ip", "link", "show", interface])
        if result.returncode == 0:
            match = MAC_EXTRACT.search(result.stdout)
            if match:
                return normalize_mac(match.group(0))

    result = run_command(["ifconfig", interface])
    if result.returncode == 0:
        match = MAC_EXTRACT.search(result.stdout)
        if match:
            return normalize_mac(match.group(0))

    print(f"[-] Could not retrieve MAC for interface: {interface}")
    sys.exit(1)


def change_mac_linux(interface, new_mac):
    """Change MAC address on Linux using *ip* or *ifconfig*."""
    use_ip = _has_ip_command()

    print(f"[+] Bringing down interface {interface}...")
    if use_ip:
        result = run_command(["ip", "link", "set", "dev", interface, "down"])
    else:
        result = run_command(["ifconfig", interface, "down"])
    if result.returncode != 0:
        print(f"[-] Failed to bring down {interface}. Are you root?")
        sys.exit(1)

    print(f"[+] Changing MAC address of {interface} to {new_mac}...")
    if use_ip:
        result = run_command(
            ["ip", "link", "set", "dev", interface, "address", new_mac]
        )
    else:
        result = run_command(["ifconfig", interface, "hw", "ether", new_mac])

    if result.returncode != 0:
        print("[-] Failed to change MAC address.")
        # Attempt to restore the interface
        if use_ip:
            run_command(["ip", "link", "set", "dev", interface, "up"])
        else:
            run_command(["ifconfig", interface, "up"])
        sys.exit(1)

    print(f"[+] Bringing up interface {interface}...")
    if use_ip:
        run_command(["ip", "link", "set", "dev", interface, "up"])
    else:
        run_command(["ifconfig", interface, "up"])
    print("[+] Done.")


# ---------------------------------------------------------------------------
# macOS (Darwin)
# ---------------------------------------------------------------------------

def get_current_mac_darwin(interface):
    """Retrieve the current MAC address on macOS."""
    result = run_command(["ifconfig", interface])
    if result.returncode != 0:
        print(f"[-] Interface not found: {interface}")
        sys.exit(1)
    match = MAC_EXTRACT.search(result.stdout)
    if not match:
        print(f"[-] Could not find MAC address for interface: {interface}")
        sys.exit(1)
    return normalize_mac(match.group(0))


def change_mac_darwin(interface, new_mac):
    """Change MAC address on macOS."""
    print(f"[+] Bringing down interface {interface}...")
    result = run_command(["ifconfig", interface, "down"])
    if result.returncode != 0:
        print(f"[-] Failed to bring down {interface}. Are you root?")
        sys.exit(1)

    print(f"[+] Changing MAC address of {interface} to {new_mac}...")
    result = run_command(["ifconfig", interface, "ether", new_mac])
    if result.returncode != 0:
        # Some macOS versions use 'lladdr' instead
        result = run_command(["ifconfig", interface, "lladdr", new_mac])
    if result.returncode != 0:
        print("[-] Failed to change MAC address.")
        run_command(["ifconfig", interface, "up"])
        sys.exit(1)

    print(f"[+] Bringing up interface {interface}...")
    run_command(["ifconfig", interface, "up"])
    print("[+] Done.")


# ---------------------------------------------------------------------------
# Windows
# ---------------------------------------------------------------------------

def get_current_mac_windows(interface):
    """Retrieve the current MAC address on Windows."""
    result = run_command([
        "powershell", "-Command",
        f'(Get-NetAdapter -Name "{interface}").MacAddress',
    ])
    if result.returncode == 0 and result.stdout.strip():
        return normalize_mac(result.stdout.strip())

    # Fallback: parse getmac output
    result = run_command(["getmac", "/v", "/fo", "csv"])
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            if interface.lower() in line.lower():
                match = MAC_EXTRACT.search(line.replace("-", ":"))
                if match:
                    return normalize_mac(match.group(0))

    print(f"[-] Interface not found: {interface}")
    sys.exit(1)


def _find_adapter_registry_key(interface):
    """Locate the registry sub-key for *interface* and return (key, desc)."""
    import winreg  # available only on Windows

    base = r"SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    # Resolve friendly name -> InterfaceDescription via PowerShell
    candidates = [interface]
    ps = run_command([
        "powershell", "-Command",
        f'(Get-NetAdapter -Name "{interface}").InterfaceDescription',
    ])
    if ps.returncode == 0 and ps.stdout.strip():
        candidates.append(ps.stdout.strip())

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base) as root:
            count = winreg.QueryInfoKey(root)[0]
            for i in range(count):
                sub_name = winreg.EnumKey(root, i)
                sub_path = f"{base}\\{sub_name}"
                try:
                    with winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        sub_path,
                        0,
                        winreg.KEY_READ | winreg.KEY_SET_VALUE,
                    ) as sub:
                        try:
                            desc = winreg.QueryValueEx(sub, "DriverDesc")[0]
                        except FileNotFoundError:
                            continue
                        for cand in candidates:
                            if (
                                cand.lower() in desc.lower()
                                or desc.lower() in cand.lower()
                            ):
                                return sub, desc
                except PermissionError:
                    continue
    except PermissionError:
        print("[-] Permission denied. Run as Administrator.")
        sys.exit(1)

    return None, None


def change_mac_windows(interface, new_mac):
    """Change MAC address on Windows via the registry and adapter restart."""
    import winreg  # standard lib, Windows-only

    mac_no_sep = new_mac.replace(":", "").replace("-", "")

    print(f"[+] Searching for adapter '{interface}' in registry...")
    key, desc = _find_adapter_registry_key(interface)
    if key is None:
        print(f"[-] Could not find adapter '{interface}' in registry.")
        sys.exit(1)

    print(f"[+] Found adapter: {desc}")
    print(f"[+] Setting MAC address to {new_mac}...")
    winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, mac_no_sep)
    winreg.CloseKey(key)

    # Restart adapter so the new MAC takes effect
    print(f"[+] Restarting adapter {interface}...")
    result = run_command([
        "powershell", "-Command",
        (
            f'Disable-NetAdapter -Name "{interface}" -Confirm:$false; '
            f"Start-Sleep -Seconds 2; "
            f'Enable-NetAdapter -Name "{interface}" -Confirm:$false'
        ),
    ])
    if result.returncode != 0:
        # Fallback with netsh
        run_command(["netsh", "interface", "set", "interface", interface, "disabled"])
        time.sleep(2)
        run_command(["netsh", "interface", "set", "interface", interface, "enabled"])
    print("[+] Done.")


# ---------------------------------------------------------------------------
# Dispatch layer
# ---------------------------------------------------------------------------

_OS = platform.system()

_GET_MAC = {
    "Linux": get_current_mac_linux,
    "Darwin": get_current_mac_darwin,
    "Windows": get_current_mac_windows,
}

_CHANGE_MAC = {
    "Linux": change_mac_linux,
    "Darwin": change_mac_darwin,
    "Windows": change_mac_windows,
}


def get_current_mac(interface):
    """Retrieve current MAC address (OS-aware)."""
    fn = _GET_MAC.get(_OS)
    if fn is None:
        print(f"[-] Unsupported operating system: {_OS}")
        sys.exit(1)
    return fn(interface)


def change_mac(interface, new_mac):
    """Change MAC address (OS-aware)."""
    fn = _CHANGE_MAC.get(_OS)
    if fn is None:
        print(f"[-] Unsupported operating system: {_OS}")
        sys.exit(1)
    fn(interface, new_mac)


def verify_mac_change(interface, expected_mac):
    """Return True if the interface now has *expected_mac*."""
    current = get_current_mac(interface)
    if current == expected_mac:
        print(f"[+] MAC address successfully verified: {current}")
        return True
    print("[-] MAC change verification failed.")
    print(f"    Expected: {expected_mac}")
    print(f"    Current:  {current}")
    return False


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv=None):
    """Parse arguments, validate, and change the MAC address."""
    args = parse_args(argv)
    new_mac = validate_mac(args.new_mac)

    # Request elevation before any privileged operations
    if not args.no_elevate:
        ensure_elevated()

    print(f"[+] Operating system: {_OS}")
    print(f"[+] Target interface: {args.interface}")

    current_mac = get_current_mac(args.interface)
    print(f"[+] Current MAC address: {current_mac}")

    if current_mac == new_mac:
        print("[*] MAC address is already set to the requested value.")
        sys.exit(0)

    change_mac(args.interface, new_mac)
    verify_mac_change(args.interface, new_mac)


if __name__ == "__main__":
    main()
