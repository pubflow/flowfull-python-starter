#!/usr/bin/env python3
"""
Generate PASETO Private Key

This script generates a new PASETO v4 private key for use with trust tokens.
The generated key should be added to your .env file as PASETO_PRIVATE_KEY.

Usage:
    python scripts/generate_paseto_key.py
"""

from pyseto import Key


def generate_paseto_key() -> None:
    """Generate and display a new PASETO v4 private key."""
    print("🔑 Generating PASETO v4 Private Key...\n")

    # Generate Ed25519 key pair for PASETO v4
    private_key = Key.new(version=4, purpose="local", key=None)

    # Convert to PASERK format
    paserk = private_key.to_paserk()

    print("=" * 80)
    print("PASETO PRIVATE KEY GENERATED")
    print("=" * 80)
    print()
    print("Add this to your .env file:")
    print()
    print(f"PASETO_PRIVATE_KEY={paserk}")
    print()
    print("=" * 80)
    print()
    print("⚠️  IMPORTANT SECURITY NOTES:")
    print("   - Keep this key SECRET and SECURE")
    print("   - Never commit this key to version control")
    print("   - Use different keys for development and production")
    print("   - Rotate keys periodically for security")
    print()
    print("=" * 80)


if __name__ == "__main__":
    generate_paseto_key()

