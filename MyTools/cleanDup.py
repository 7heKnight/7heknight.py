"""
Duplicate file cleaner — scans a directory tree, hashes every file, and
removes duplicates (keeping the first occurrence). Produces a log file
in the target directory.

Usage:
    python cleanDup.py <directory> [--dry-run] [--log-file <path>]

Flags:
    --dry-run    List duplicates without deleting them.
    --log-file   Custom path for the log file (default: <directory>/cleanup.log).
"""

import argparse
import hashlib
import logging
import os
import sys
import time

CHUNK_SIZE = 8192  # bytes read per iteration when hashing


def make_hash(filepath, algorithm="sha256"):
    """Return the hex-digest hash of *filepath*, reading in chunks."""
    hasher = hashlib.new(algorithm)
    with open(filepath, "rb") as fh:
        while True:
            chunk = fh.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_directory(directory, dry_run=False):
    """Walk *directory*, remove (or report) duplicate files.

    Returns (removed_count, scanned_count, errors_count).
    """
    seen_hashes = set()
    removed = 0
    scanned = 0
    errors = 0

    for root, _dirs, files in os.walk(directory, topdown=True):
        if files:
            logging.info("Scanning directory: %s", root)

        for name in files:
            filepath = os.path.join(root, name)

            # Skip symlinks to avoid unintended deletions
            if os.path.islink(filepath):
                logging.debug("Skipping symlink: %s", filepath)
                continue

            try:
                file_hash = make_hash(filepath)
                scanned += 1
            except OSError as exc:
                errors += 1
                logging.warning("Could not read file: %s (%s)", filepath, exc)
                continue

            if file_hash not in seen_hashes:
                seen_hashes.add(file_hash)
            else:
                if dry_run:
                    logging.info("[DRY-RUN] Would remove duplicate: %s", filepath)
                else:
                    try:
                        os.remove(filepath)
                        logging.info("Removed duplicate: %s", filepath)
                    except OSError as exc:
                        errors += 1
                        logging.warning("Could not remove file: %s (%s)", filepath, exc)
                        continue
                removed += 1

    return removed, scanned, errors


def _build_parser():
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Find and remove duplicate files in a directory tree.",
    )
    parser.add_argument(
        "directory",
        help="Root directory to scan for duplicates.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Report duplicates without deleting them.",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Path for the log file (default: <directory>/cleanup.log).",
    )
    return parser


def _configure_logging(log_path):
    """Set up logging to both console and *log_path*."""
    fmt = "%(asctime)s  %(levelname)-8s  %(message)s"
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_path, encoding="utf-8"),
    ]
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=handlers)


def main(args=None):
    """Entry point for the duplicate-file cleaner."""
    parser = _build_parser()
    opts = parser.parse_args(args)

    directory = os.path.abspath(opts.directory)
    if not os.path.isdir(directory):
        parser.error(f"Not a valid directory: {directory}")

    log_path = opts.log_file or os.path.join(directory, "cleanup.log")
    _configure_logging(log_path)

    logging.info("Starting scan: %s (dry_run=%s)", directory, opts.dry_run)
    start = time.time()

    removed, scanned, errors = scan_directory(directory, dry_run=opts.dry_run)

    elapsed = time.time() - start
    logging.info("Scanned %d files in %.2f sec", scanned, elapsed)
    if errors:
        logging.info("Encountered %d error(s)", errors)
    if removed == 0:
        logging.info("No duplicate files found.")
    else:
        action = "Would remove" if opts.dry_run else "Removed"
        logging.info("%s %d duplicate file(s).", action, removed)

    return 0


if __name__ == "__main__":
    sys.exit(main())
        

