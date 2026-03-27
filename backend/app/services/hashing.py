import hashlib

def hash_file(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

