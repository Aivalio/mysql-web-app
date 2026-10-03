"""Generate a Werkzeug password hash for the ADMIN_PASSWORD_HASH config value.

Usage:
    python scripts/generate_password_hash.py
    python scripts/generate_password_hash.py "your secret password"

The printed hash goes into your .env as:
    ADMIN_PASSWORD_HASH=scrypt:...
"""
import getpass
import sys

from werkzeug.security import generate_password_hash


def main() -> int:
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = getpass.getpass("Admin password (hidden): ")
        if not password:
            print("No password given.", file=sys.stderr)
            return 1

    print(generate_password_hash(password))
    print(
        "\nPaste the line above into your .env as ADMIN_PASSWORD_HASH=... "
        "(keep it in one line).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())