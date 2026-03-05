#!/usr/bin/env python3
"""Command-line password generator using cryptographically secure randomness."""

import secrets
import string
import sys

# Character pools
DIGITS = string.digits
LETTERS = string.ascii_letters
SPECIAL = string.punctuation
DEFAULT_CHARSET = DIGITS + LETTERS + SPECIAL

MIN_LENGTH = 4  # Minimum to guarantee one char from each required category


def generate_password(length, *, use_special=True):
    """Generate a cryptographically secure random password of the given length.

    Guarantees at least one uppercase letter, one lowercase letter, one digit,
    and (optionally) one special character.

    Args:
        length: Desired password length (minimum 4).
        use_special: Include special/punctuation characters (default True).

    Returns:
        A random password string.

    Raises:
        TypeError: If length is not an integer.
        ValueError: If length is below the minimum.
    """
    if not isinstance(length, int):
        raise TypeError(f"length must be an integer, got {type(length).__name__}")
    if length < MIN_LENGTH:
        raise ValueError(
            f"Password length must be at least {MIN_LENGTH}, got {length}"
        )

    charset = DEFAULT_CHARSET if use_special else (DIGITS + LETTERS)

    # Guarantee at least one character from each required category
    required = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(DIGITS),
    ]
    if use_special:
        required.append(secrets.choice(SPECIAL))

    # Fill remaining length from the full charset
    remaining = length - len(required)
    rest = [secrets.choice(charset) for _ in range(remaining)]

    # Combine and shuffle to avoid predictable positions
    password_chars = required + rest
    # Fisher-Yates shuffle using secrets for unbiased ordering
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def main(argv=None):
    """CLI entry point for password generation."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print(
            f"Usage: {sys.argv[0]} <length> [--no-special]\n"
            f"  length       Password length (integer >= {MIN_LENGTH})\n"
            f"  --no-special Exclude special characters",
            file=sys.stderr,
        )
        sys.exit(1)

    use_special = "--no-special" not in argv
    length_args = [a for a in argv if not a.startswith("--")]

    if not length_args:
        print("[-] Missing length argument.", file=sys.stderr)
        sys.exit(1)

    try:
        length = int(length_args[0])
    except ValueError:
        print("[-] Length must be an integer.", file=sys.stderr)
        sys.exit(1)

    try:
        password = generate_password(length, use_special=use_special)
    except (TypeError, ValueError) as exc:
        print(f"[-] {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Generated password: {password}")


if __name__ == "__main__":
    main()
