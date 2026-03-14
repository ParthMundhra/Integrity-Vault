from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import status

from app.services import hashing

router = APIRouter()


@router.post(
    "/evidence/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload and register new evidence",
)
async def upload_evidence(file: UploadFile = File(...)) -> dict:
    """
    Receive an evidence file, compute its hash, and queue it for registration.

    In a full implementation this endpoint will:
    - Stream the file to secure off-chain storage.
    - Compute a SHA-256 hash of the file contents.
    - Persist metadata to PostgreSQL.
    - Submit a transaction to the Ethereum smart contract.
    """
    content = await file.read()
    file_hash = hashing.compute_sha256(content)

    # Placeholder response; persistence and blockchain integration to be added.
    return {
        "message": "Evidence received (placeholder).",
        "filename": file.filename,
        "sha256": file_hash,
    }


@router.get(
    "/evidence/{evidence_id}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve evidence metadata by ID",
)
async def get_evidence(evidence_id: str) -> dict:
    """
    Retrieve evidence metadata by its identifier.

    In a full implementation this endpoint will:
    - Query PostgreSQL for evidence metadata and status.
    - Optionally return pointers to off-chain storage (never raw evidence by default).
    - Cross-reference blockchain transaction hashes for this evidence ID.
    """
    # Placeholder implementation.
    if not evidence_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Evidence ID must be provided.",
        )

    return {
        "evidence_id": evidence_id,
        "status": "placeholder",
        "details": "Evidence lookup not yet implemented.",
    }


@router.post(
    "/evidence/verify",
    status_code=status.HTTP_200_OK,
    summary="Verify evidence integrity against stored hash",
)
async def verify_evidence(file: UploadFile = File(...)) -> dict:
    """
    Verify the integrity of an evidence file.

    In a full implementation this endpoint will:
    - Compute the file's SHA-256 hash.
    - Look up the canonical hash for this evidence from PostgreSQL / blockchain.
    - Return a match/mismatch result and relevant blockchain references.
    """
    content = await file.read()
    file_hash = hashing.compute_sha256(content)

    # Placeholder comparison; no stored hash is checked yet.
    return {
        "sha256": file_hash,
        "verified": False,
        "details": "Verification logic not yet implemented.",
    }

