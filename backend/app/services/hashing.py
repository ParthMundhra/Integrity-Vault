import hashlib
from typing import Union


def compute_sha256(data: Union[bytes, bytearray]) -> str:
    """
    Compute a SHA-256 hash for the given binary data and return it as hex.

    This helper is used for:
    - Evidence file hashing at upload time.
    - Integrity verification when recomputing hashes for comparison with
      stored values in PostgreSQL and on the blockchain.
    """
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

