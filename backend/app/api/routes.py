import logging
import os
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Evidence
from app.services.blockchain import register_on_chain, verify_on_chain
from app.services.hashing import hash_file

router = APIRouter()
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
storage_path = os.path.join(BASE_DIR, "storage")
os.makedirs(storage_path, exist_ok=True)


def success_response(data: dict, status_code: int = 200) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"status": "success", "data": data})


def error_response(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"status": "error", "message": message})


def is_valid_uuid(value: str) -> bool:
    try:
        UUID(value)
        return True
    except ValueError:
        return False


@router.post("/evidence/upload")
async def upload_evidence(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file is None or not file.filename:
        return error_response("No file was provided", 400)

    content = await file.read()
    if not content:
        return error_response("Uploaded file is empty", 400)

    try:
        file_hash = hash_file(content)
        original_name = os.path.basename(file.filename)

        evidence = Evidence(
            file_name=original_name,
            hash=file_hash,
        )

        db.add(evidence)
        db.flush()

        file_path = os.path.join(storage_path, f"{evidence.id}_{original_name}")
        with open(file_path, "wb") as file_handle:
            file_handle.write(content)

        evidence.file_path = file_path
        db.commit()
        db.refresh(evidence)
    except Exception as exc:
        logger.exception("Failed to store evidence: %s", exc)
        db.rollback()
        if "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return error_response("Failed to store evidence", 500)

    blockchain_tx = None
    try:
        blockchain_tx = register_on_chain(file_hash)
    except Exception as exc:
        logger.exception("Blockchain registration failed for evidence %s: %s", evidence.id, exc)

    return success_response(
        {
            "evidence_id": evidence.id,
            "file_name": evidence.file_name,
            "hash": evidence.hash,
            "file_path": evidence.file_path,
            "blockchain_tx": blockchain_tx,
        },
        status_code=201,
    )


@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: str, db: Session = Depends(get_db)):
    if not is_valid_uuid(evidence_id):
        return error_response("Invalid evidence_id format", 400)

    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        return error_response("Evidence not found", 404)

    return success_response(
        {
            "evidence_id": evidence.id,
            "file_name": evidence.file_name,
            "hash": evidence.hash,
            "file_path": evidence.file_path,
        }
    )


@router.post("/evidence/verify")
async def verify_stored_evidence(
    evidence_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not is_valid_uuid(evidence_id):
        return error_response("Invalid evidence_id format", 400)

    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        return error_response("Evidence not found", 404)

    original_hash = evidence.hash

    # Defensive reset to ensure the uploaded stream is read from the beginning.
    await file.seek(0)
    content = await file.read()
    if not content:
        return error_response("Empty file received", 400)

    new_hash = hash_file(content)
    db_verification = "VERIFIED" if new_hash == original_hash else "TAMPERED"

    blockchain_verification = False
    try:
        blockchain_verification = verify_on_chain(new_hash)
    except Exception as exc:
        logger.exception("Blockchain verification failed for evidence %s: %s", evidence.id, exc)

    return success_response(
        {
            "db_verification": db_verification,
            "blockchain_verification": blockchain_verification,
        }
    )