"""WiFi password extractor for Windows.

Uses `netsh wlan` to retrieve stored WiFi profile names and their passwords.
Requires administrator privileges and a Windows operating system.
"""

import ctypes
import json
import os
import re
import sys
from subprocess import check_output, CalledProcessError

PASSWORD_LOG_FILE = "ListWifiPassword.txt"

# Regex patterns for parsing netsh output
PROFILE_PATTERN = re.compile(r"All User Profile\s*:\s*(.+)")
KEY_CONTENT_PATTERN = re.compile(r"Key Content\s*:\s*(.+)")


def is_admin():
    """Return True if the current process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        # ctypes.windll is unavailable on non-Windows platforms
        return False


def is_windows():
    """Return True if running on a Windows platform."""
    return sys.platform.startswith("win")


def load_saved_passwords(filepath=PASSWORD_LOG_FILE):
    """Load previously saved passwords from the log file, if it exists."""
    if not os.path.isfile(filepath):
        return set()
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            return {line for line in fh.read().splitlines() if line.strip()}
    except OSError:
        return set()


def save_new_passwords(passwords, filepath=PASSWORD_LOG_FILE):
    """Append newly discovered passwords to the log file, skipping duplicates."""
    existing = load_saved_passwords(filepath)
    new_entries = [p for p in passwords if p not in existing]
    if not new_entries:
        return
    with open(filepath, "a", encoding="utf-8") as fh:
        for entry in new_entries:
            fh.write(entry + "\n")


def get_profile_names():
    """Return a list of all stored WiFi profile names."""
    try:
        output = check_output(
            ["netsh", "wlan", "show", "profile"],
            encoding="utf-8",
            errors="replace",
        )
    except (CalledProcessError, FileNotFoundError) as exc:
        sys.exit(f"[-] Failed to list WiFi profiles: {exc}")

    profiles = [m.group(1).strip() for m in PROFILE_PATTERN.finditer(output)]
    return profiles


def get_password(profile_name):
    """Return the password for *profile_name*, or None if unavailable."""
    try:
        output = check_output(
            ["netsh", "wlan", "show", "profile", profile_name, "key=clear"],
            encoding="utf-8",
            errors="replace",
        )
    except CalledProcessError:
        return None
    except FileNotFoundError:
        sys.exit("[-] 'netsh' command not found. Are you on Windows?")

    match = KEY_CONTENT_PATTERN.search(output)
    return match.group(1).strip() if match else None


def show_all_profiles(output_json=False):
    """Retrieve and display passwords for every stored WiFi profile."""
    profiles = get_profile_names()
    if not profiles:
        print("[-] No WiFi profiles found.")
        return

    results = []
    for name in profiles:
        password = get_password(name)
        if password is not None:
            results.append({"interface": name, "password": password})

    if output_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        if not results:
            print("[-] No passwords could be retrieved.")
            return
        print("\n--- Result ---\n")
        for entry in results:
            print(f"Interface: {entry['interface']}")
            print(f"Password:  {entry['password']}")
            print()

    save_new_passwords([r["password"] for r in results])


def show_single_profile(profile_name, output_json=False):
    """Retrieve and display the password for a single WiFi profile."""
    password = get_password(profile_name)

    if password is None:
        message = f'[-] Password for "{profile_name}" not found.'
        if output_json:
            print(json.dumps({"error": message}, indent=2))
        else:
            print(message)
        return

    if output_json:
        print(json.dumps({"interface": profile_name, "password": password}, indent=2))
    else:
        print("\n--- Result ---\n")
        print(f"Interface: {profile_name}")
        print(f"Password:  {password}")
        print()

    save_new_passwords([password])


def print_help():
    """Print usage information."""
    script = os.path.basename(sys.argv[0])
    print(
        f"\nWiFi Password Extractor — lists saved WiFi passwords (Windows only)\n"
        f"\nUsage:\n"
        f"  python {script}                     Show all profiles and passwords\n"
        f"  python {script} <profile_name>      Show password for a specific profile\n"
        f"  python {script} --json              Show all profiles in JSON format\n"
        f"  python {script} <profile> --json    Show one profile in JSON format\n"
        f"  python {script} -h | --help         Show this help message\n"
    )


def parse_args(argv):
    """Parse command-line arguments and return (profile_name, json_flag, help_flag)."""
    args = argv[1:]
    help_flag = False
    json_flag = False
    profile_name = None

    for arg in args:
        if arg in ("-h", "--help"):
            help_flag = True
        elif arg == "--json":
            json_flag = True
        elif profile_name is None:
            profile_name = arg
        else:
            sys.exit(
                f'[-] Unexpected argument: "{arg}"\n'
                f'    If the profile name contains spaces, wrap it in quotes.'
            )

    return profile_name, json_flag, help_flag


def main():
    """Entry point: validates environment, parses args, and dispatches commands."""
    if not is_windows():
        sys.exit("[-] This tool requires Windows (uses netsh).")

    if not is_admin():
        sys.exit("[-] Access denied. Run this script as Administrator.")

    profile_name, json_flag, help_flag = parse_args(sys.argv)

    if help_flag:
        print_help()
        return

    if profile_name:
        show_single_profile(profile_name, output_json=json_flag)
    else:
        show_all_profiles(output_json=json_flag)

    print("-------------------------------------------")
    print("[+] Program executed successfully.")


if __name__ == "__main__":
    main()
