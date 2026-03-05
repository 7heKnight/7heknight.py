"""File finder utility — searches directories by name, extension, and content."""

import argparse
import os
import re
import sys
from typing import List, Optional


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Search for files by name, extension, or content.",
        usage="%(prog)s [-d DIRECTORY] [-n NAME] [-f TYPE] [--content PATTERN]",
    )
    parser.add_argument("-d", metavar="DIRECTORY", default=None,
                        help="Root directory to search (default: current directory).")
    parser.add_argument("-f", metavar="TYPE", default=None,
                        help="File extension to match (e.g. .py, .txt).")
    parser.add_argument("-n", metavar="NAME", default=None,
                        help="Substring or regex pattern to match against the file name.")
    parser.add_argument("--content", metavar="PATTERN", default=None,
                        help="Regex pattern to search inside file contents (may be slow on large trees).")
    opts = parser.parse_args(argv)
    if not opts.f and not opts.n and not opts.content:
        parser.error("At least one of -n, -f, or --content is required.")
    return opts


def resolve_directory(directory: Optional[str]) -> str:
    """Return an absolute, normalised directory path (defaults to cwd)."""
    if not directory:
        return os.getcwd()
    resolved = os.path.abspath(os.path.expanduser(directory))
    if not os.path.isdir(resolved):
        raise FileNotFoundError(f"Directory not found: {resolved}")
    return resolved


def _compile_name_pattern(file_name: Optional[str], file_type: Optional[str]) -> re.Pattern:
    """Build a compiled regex that matches against a bare filename."""
    name_part = file_name if file_name else ".*"
    type_part = re.escape(file_type) if file_type else ".*"
    # Match: <name_part> followed by anything, ending with <type_part>
    pattern = name_part + r".*" + type_part + r"$"
    try:
        return re.compile(pattern, re.IGNORECASE)
    except re.error as exc:
        raise ValueError(f"Invalid regex in name/type filter: {exc}") from exc


def content_matches(filepath: str, pattern: re.Pattern) -> bool:
    """Return True if *pattern* matches anywhere inside *filepath*'s text."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if pattern.search(line):
                    return True
    except (OSError, IOError):
        # Unreadable file (permissions, broken symlink, etc.) — skip silently
        pass
    return False


def find(
    directory: Optional[str] = None,
    file_type: Optional[str] = None,
    file_name: Optional[str] = None,
    content: Optional[str] = None,
) -> List[str]:
    """Walk *directory* and return paths matching the given filters.

    Filters are combined with AND logic: a file must satisfy all supplied
    criteria (name, type, content) to be included in results.
    """
    root_dir = resolve_directory(directory)
    name_re = _compile_name_pattern(file_name, file_type)

    content_re: Optional[re.Pattern] = None
    if content:
        try:
            content_re = re.compile(content, re.IGNORECASE)
        except re.error as exc:
            raise ValueError(f"Invalid content regex: {exc}") from exc

    results: List[str] = []

    try:
        for dirpath, _dirnames, filenames in os.walk(root_dir, topdown=True):
            for fname in filenames:
                if not name_re.search(fname):
                    continue
                full_path = os.path.join(dirpath, fname)
                if content_re and not content_matches(full_path, content_re):
                    continue
                results.append(full_path)
    except KeyboardInterrupt:
        print("\n[-] Terminated.", file=sys.stderr)

    return results


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for CLI usage."""
    opts = parse_args(argv)

    if opts.content:
        print(f'\n[*] Searching with content: "{opts.content}"\n')
    else:
        print("[*] Searching...\n")

    try:
        matches = find(opts.d, opts.f, opts.n, opts.content)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[-] {exc}", file=sys.stderr)
        return 1

    if not matches:
        print("[-] No result found.")
        return 1

    for filepath in matches:
        print(filepath)

    print("----------------------------------")
    print(f"[+] Program executed successfully with {len(matches)} result(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
