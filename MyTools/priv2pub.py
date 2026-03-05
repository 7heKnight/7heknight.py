from argparse import ArgumentParser
from shutil import which
from subprocess import CalledProcessError, run
from sys import exit


def normalize_private_key(value: str) -> str:
    """Return a PEM-formatted RSA private key from raw or PEM input text."""
    if value is None:
        raise ValueError("Private key is required.")

    text = value.strip()
    if not text:
        raise ValueError("Private key cannot be empty.")

    rsa_begin = "-----BEGIN RSA PRIVATE KEY-----"
    rsa_end = "-----END RSA PRIVATE KEY-----"
    generic_begin = "-----BEGIN PRIVATE KEY-----"
    generic_end = "-----END PRIVATE KEY-----"

    if (rsa_begin in text and rsa_end in text) or (generic_begin in text and generic_end in text):
        return text if text.endswith("\n") else f"{text}\n"

    return f"{rsa_begin}\n{text}\n{rsa_end}\n"


def extract_public_key(private_key_text: str) -> str:
    """Generate and return the public key PEM using local OpenSSL."""
    if which("openssl") is None:
        raise RuntimeError("OpenSSL is not installed or not in PATH.")

    pem = normalize_private_key(private_key_text)

    try:
        completed = run(
            ["openssl", "rsa", "-pubout"],
            input=pem,
            text=True,
            capture_output=True,
            check=True,
        )
    except CalledProcessError as error:
        details = (error.stderr or error.stdout or "").strip()
        message = details or "OpenSSL failed to parse the private key."
        raise ValueError(message) from error

    return completed.stdout.strip()


def parse_args() -> str:
    """Parse command-line arguments and return the provided key value."""
    parser = ArgumentParser(description="Extract RSA public key from private key input.")
    parser.add_argument("private_key", help="RSA private key body or full PEM text.")
    return parser.parse_args().private_key


if __name__ == '__main__':
    try:
        print(extract_public_key(parse_args()))
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")
        exit(1)
