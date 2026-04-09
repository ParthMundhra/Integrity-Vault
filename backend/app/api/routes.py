import logging
import os
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Evidence
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

    return success_response(
        {
            "evidence_id": evidence.id,
            "file_name": evidence.file_name,
            "hash": evidence.hash,
            "file_path": evidence.file_path,
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


@router.get("/evidence/verify/{evidence_id}")
def verify_stored_evidence(evidence_id: str, db: Session = Depends(get_db)):
    if not is_valid_uuid(evidence_id):
        return error_response("Invalid evidence_id format", 400)

    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        return error_response("Evidence not found", 404)
    if not evidence.file_path:
        return error_response("Evidence file path is missing", 500)

    if not os.path.exists(evidence.file_path):
        return error_response("Stored evidence file not found on disk", 404)

    with open(evidence.file_path, "rb") as file_handle:
        content = file_handle.read()
    if not content:
        return error_response("Stored evidence file is empty", 400)

    current_hash = hash_file(content)
    verification_status = "VERIFIED" if current_hash == evidence.hash else "TAMPERED"

    return success_response(
        {
            "evidence_id": evidence.id,
            "verification_status": verification_status,
            "stored_hash": evidence.hash,
            "current_hash": current_hash,
        }
    )