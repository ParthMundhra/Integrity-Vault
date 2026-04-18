## Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System

This repository contains a reference implementation of a **secure digital forensics evidence management platform** backed by **Ethereum**. The system is designed to make the collection, storage, transfer, and verification of digital evidence:

- **Tamper‑evident** – Any modification to evidence is detectable via cryptographic hashes.
- **Traceable** – Every custody action is recorded as an immutable blockchain event.
- **Auditable** – Investigators and auditors can reconstruct complete custody timelines.

Raw evidence files are stored **off‑chain** in encrypted storage, while **cryptographic hashes and custody events** are recorded on the blockchain.

---

## System Architecture Summary

At a high level, the system consists of:

- **Backend (FastAPI / Python)**
  - Exposes REST APIs for evidence upload, retrieval, and verification.
  - Computes SHA‑256 hashes and orchestrates AES encryption of off‑chain evidence.
  - Persists metadata and references in PostgreSQL.
  - Interacts with the Ethereum smart contract to register evidence and log custody events.

- **Blockchain Layer (Ethereum / Solidity)**
  - `EvidenceCustody` contract stores:
    - Evidence registration records (IDs and hashes).
    - Custody events for collect, transfer, view, verify, and release actions.
  - Ganache (or similar) is used for local development and testing.

- **Frontend (React / Vite)**
  - Investigator and auditor dashboard for:
    - Uploading evidence.
    - Viewing custody timelines.
    - Verifying evidence integrity.

- **Database (PostgreSQL)**
  - Stores evidence metadata, user and case information, and references to blockchain transactions and off‑chain storage.

- **Docker & DevOps**
  - Dockerfiles and `docker-compose.yml` for running backend, PostgreSQL, and Ganache in a local development stack.

More detailed diagrams and explanations are available under `docs/architecture/system-architecture.md`.

---

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, PostgreSQL
- **Cryptography**: SHA‑256 hashing, AES encryption (placeholder interface), `cryptography` library (to be wired in)
- **Blockchain**: Ethereum, Solidity, Ganache (local), ethers.js (deployment placeholder)
- **Frontend**: React (Vite‑style structure), JSX components
- **DevOps**: Docker, Docker Compose

---

## Repository Structure

```text
backend/      FastAPI application, services, and DB config
blockchain/   Solidity contracts and deployment scripts
frontend/     React (Vite) UI components and pages
docker/       Dockerfile and docker-compose stack definition
docs/         Architecture, threat model, ADRs, and UI wireframes
```

See the `README.md` inside each subdirectory for more details.

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js (for future frontend work)
- Docker & Docker Compose (optional but recommended for local stack)

### Option 1: Run Backend Locally (without Docker)

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Set up a PostgreSQL instance and export `DATABASE_URL`, then run:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Option 2: Run Full Stack with Docker

From the repository root:

```bash
cd docker
docker compose up --build
```

This starts:

- `backend` on `http://localhost:8000`
- `postgres` on `localhost:5432`
- `ganache` on `http://localhost:8545`

You can then:

- Call backend endpoints such as `POST /api/evidence/upload` and `POST /api/evidence/verify`.
- Deploy and interact with the `EvidenceCustody` contract using the scripts under `blockchain/` (once wired to Hardhat/Truffle).

---

## Contribution Guidelines

- **Security first**
  - Do not commit real secrets (private keys, passwords, tokens).
  - Use environment variables or a secrets manager for sensitive configuration.
  - Prefer well‑reviewed cryptographic libraries over custom implementations.

- **Code quality**
  - Keep modules small, focused, and well‑documented.
  - Add or update tests when introducing new behavior.
  - Run linters and type checkers where configured.

- **Architecture & documentation**
  - Consult `docs/` before making significant changes to architecture, threat model, or smart contracts.
  - Capture major design decisions as new ADRs under `docs/decisions/`.

Pull requests should describe the motivation, changes made, and any security or migration considerations.
