## Backend Service (`backend/`)

The backend is a **FastAPI** service that provides the core API surface for the Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System.

It is responsible for:

- **Evidence lifecycle management**
  - Accepting evidence uploads from the frontend.
  - Orchestrating off‑chain storage and metadata persistence.
  - Providing APIs to retrieve and verify evidence.

- **Hashing & integrity**
  - Computing **SHA‑256** hashes for evidence files via `app/services/hashing.py`.
  - Recomputing hashes during verification and comparing them with stored values and blockchain records.

- **Encryption (off‑chain evidence)**
  - Defining the interface for **AES** encryption in `app/services/encryption.py`.
  - Actual key management and cryptographic implementation will be integrated with a dedicated KMS or secrets manager.

- **Database access**
  - Managing the **PostgreSQL** connection and sessions via `app/db/database.py`.
  - Persisting evidence metadata, custody references, and audit logs (models to be added).

- **Blockchain integration**
  - Coordinating with the Ethereum smart contract layer to:
    - Register evidence hashes.
    - Append custody events for actions such as collect, transfer, view, and verify.

### Structure

- `app/main.py` – FastAPI application factory and entrypoint.
- `app/api/routes.py` – API router and placeholder endpoints:
  - `POST /api/evidence/upload`
  - `GET /api/evidence/{id}`
  - `POST /api/evidence/verify`
- `app/services/hashing.py` – SHA‑256 hashing utilities for evidence data.
- `app/services/encryption.py` – AES encryption/decryption interface (placeholder).
- `app/db/database.py` – PostgreSQL engine and session helpers.
- `requirements.txt` – Python dependencies for the backend service.

The backend is designed to be **modular**, **secure‑by‑default**, and ready to be extended with authentication, authorization, detailed models, and blockchain clients.
