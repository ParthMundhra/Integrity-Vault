"""
AES encryption/decryption service placeholder.

This module defines the interface for symmetric encryption operations used to
protect off-chain evidence files. The concrete implementation should:

- Use a vetted crypto library (e.g., `cryptography`).
- Prefer AES-256-GCM or another authenticated encryption mode.
- Manage keys via a dedicated KMS or secrets manager.

The functions currently raise NotImplementedError to avoid giving a false sense
of security before a full implementation is in place.
"""

from typing import Tuple


def encrypt_evidence(plaintext: bytes) -> Tuple[bytes, bytes]:
    """
    Encrypt an evidence payload.

    Returns a tuple of (ciphertext, nonce_or_iv). In a full implementation,
    additional metadata (e.g., auth tag) may also be returned.
    """
    raise NotImplementedError("AES encryption is not yet implemented.")


def decrypt_evidence(ciphertext: bytes, nonce_or_iv: bytes) -> bytes:
    """
    Decrypt an evidence payload previously encrypted by `encrypt_evidence`.
    """
    raise NotImplementedError("AES decryption is not yet implemented.")

