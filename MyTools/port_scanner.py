"""Multithreaded TCP port scanner using only standard library modules."""

import argparse
import re
import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

MIN_PORT = 1
MAX_PORT = 65535
DEFAULT_TIMEOUT = 1.0
DEFAULT_WORKERS = 100


def parse_arguments(args=None):
    """Parse CLI arguments for hostname and port specification."""
    parser = argparse.ArgumentParser(description="TCP port scanner.")
    parser.add_argument(
        "-p",
        dest="ports",
        required=True,
        help="Comma-separated port list, e.g. 22,80,443,1-10",
    )
    parser.add_argument(
        "--host",
        dest="hostname",
        required=True,
        help="Target hostname or IP address.",
    )
    parser.add_argument(
        "-t",
        dest="timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Connection timeout in seconds (default: {DEFAULT_TIMEOUT}).",
    )
    parser.add_argument(
        "-w",
        dest="workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Max concurrent threads (default: {DEFAULT_WORKERS}).",
    )
    return parser.parse_args(args)


def sanitize_hostname(hostname):
    """Strip protocol prefix and trailing path from a hostname string."""
    hostname = re.sub(r"^[a-zA-Z][a-zA-Z0-9+\-.]*://", "", hostname)
    match = re.search(r"^([\w.\-]+)", hostname)
    if not match:
        raise ValueError(f"Invalid hostname format: {hostname!r}")
    return match.group(1)


def resolve_hostname(hostname):
    """Resolve a hostname to an IPv4 address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as exc:
        raise ConnectionError(f"Cannot resolve {hostname!r}: {exc}") from exc


def parse_ports(port_string):
    """Parse a comma-separated port specification into a sorted list of unique ints.

    Supports individual ports (80) and inclusive ranges (1-1024).
    """
    ports = set()
    segments = port_string.split(",")
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        if "-" in segment:
            parts = segment.split("-", 1)
            if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
                raise ValueError(f"Invalid port range: {segment!r}")
            try:
                start, end = int(parts[0].strip()), int(parts[1].strip())
            except ValueError:
                raise ValueError(f"Non-numeric port range: {segment!r}")
            if start > end:
                raise ValueError(
                    f"Port range start ({start}) > end ({end}) in {segment!r}"
                )
            for port in range(start, end + 1):
                _validate_port(port)
                ports.add(port)
        else:
            try:
                port = int(segment)
            except ValueError:
                raise ValueError(f"Non-numeric port: {segment!r}")
            _validate_port(port)
            ports.add(port)
    if not ports:
        raise ValueError("No valid ports specified.")
    return sorted(ports)


def _validate_port(port):
    """Raise ValueError if port is outside the valid TCP range."""
    if not (MIN_PORT <= port <= MAX_PORT):
        raise ValueError(f"Port {port} out of range ({MIN_PORT}-{MAX_PORT}).")


def scan_port(target, port, timeout=DEFAULT_TIMEOUT):
    """Attempt a TCP connect to *target*:*port*; return the port if open, else None."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((target, port))
        return port
    except (OSError, socket.timeout):
        return None
    finally:
        sock.close()


def run_scan(target, ports, timeout=DEFAULT_TIMEOUT, workers=DEFAULT_WORKERS):
    """Scan *ports* on *target* concurrently and return a sorted list of open ports."""
    open_ports = []
    lock = threading.Lock()

    def _worker(port):
        result = scan_port(target, port, timeout)
        if result is not None:
            with lock:
                open_ports.append(result)
            print(f"   [+] TCP/{port} open")

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_worker, p): p for p in ports}
        try:
            for future in as_completed(futures):
                future.result()  # propagate exceptions
        except KeyboardInterrupt:
            print("\n[-] Scan interrupted by user.")
            pool.shutdown(wait=False, cancel_futures=True)
            return sorted(open_ports)

    return sorted(open_ports)


def main(cli_args=None):
    """Entry point: parse args, resolve host, scan ports, and print results."""
    args = parse_arguments(cli_args)

    hostname = sanitize_hostname(args.hostname)
    target_ip = resolve_hostname(hostname)
    ports = parse_ports(args.ports)

    print(f"[*] Scanning {hostname} ({target_ip}) — {len(ports)} port(s) …")
    open_ports = run_scan(target_ip, ports, args.timeout, args.workers)

    print("----------------------------------")
    if open_ports:
        print(f"[+] {len(open_ports)} open port(s) found.")
    else:
        print("[*] No open ports found.")
    print("Scan completed successfully.")
    return open_ports


if __name__ == "__main__":
    try:
        main()
    except (ValueError, ConnectionError) as exc:
        print(f"[-] Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[-] Keyboard Interruption: Terminated!")
        sys.exit(130)
