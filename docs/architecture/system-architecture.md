## System Architecture

This document describes the high-level architecture for the **Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System**. The goal of the system is to preserve the integrity, authenticity, and traceability of digital evidence across its entire lifecycle, from initial collection to presentation in court or internal investigations.

The architecture is designed around the following principles:

- **Integrity**: Evidence and custody events must be tamper‑evident.
- **Traceability**: Every action on evidence must be recorded and auditable.
- **Least privilege**: Access to evidence and custody actions must be tightly controlled.
- **Separation of concerns**: Evidence data is stored off‑chain; cryptographic proofs and custody records are stored on‑chain.

---

## High‑Level Components

- **Frontend (React + Vite)**
  - Web UI for investigators, lab personnel, and auditors.
  - Provides workflows for evidence upload, custody transfer, viewing history, and integrity verification.
  - Communicates with the backend via secure HTTPS APIs.
  - Interacts with the Ethereum network (via backend or a gateway) for reading custody records and submitting transactions.

- **Backend API (FastAPI, Python 3.11)**
  - Central application server that implements business logic and authorization.
  - Exposes REST/JSON (and optionally WebSocket) endpoints to the frontend.
  - Manages evidence metadata, user roles, and access control.
  - Handles cryptographic operations (SHA‑256 hashing, AES encryption/decryption).
  - Orchestrates blockchain writes/reads through an Ethereum client or web3 provider.
  - Interfaces with the PostgreSQL database and off‑chain evidence storage.

- **Database (PostgreSQL)**
  - Stores structured metadata about:
    - Evidence records (IDs, descriptions, case references, file locations, hash values, status).
    - Custody events (linked to on‑chain transaction hashes, but also cached for querying).
    - Users, roles, permissions, and audit logs.
  - Acts as the system of record for operational data that does not require on‑chain immutability, while remaining consistent with blockchain state.

- **Off‑Chain Evidence Storage**
  - Secure file storage (e.g., encrypted file store, S3‑compatible storage, or on‑premises storage) for raw evidence files.
  - Files are **encrypted at rest** using AES (e.g., AES‑256‑GCM) with keys managed by the backend or a dedicated KMS.
  - Only cryptographic hashes (SHA‑256) of the files and metadata are used on‑chain.

- **Blockchain Layer (Ethereum, Solidity, Ganache in development)**
  - Smart contracts store:
    - Evidence registration records (evidence ID, content hash, metadata hash).
    - Immutable custody events (who performed which action, when, under which case).
  - Ethereum test environment (Ganache) is used for local development and testing.
  - In production, this could target a permissioned or consortium Ethereum network.

- **DevOps / Infrastructure (Docker)**
  - All services (backend, frontend, database, Ethereum node, supporting services) are containerized.
  - Docker Compose or orchestration tooling defines reproducible development and deployment environments.
  - Enables consistent security hardening (e.g., network isolation, secrets injection) across services.

---

## Data Flow: Evidence Collection to Blockchain Record

This section describes the typical flow when new digital evidence is collected and registered in the system.

1. **Evidence Collection (User → Frontend)**
   - An authorized investigator logs into the web UI.
   - The investigator navigates to the **Evidence Upload** page and provides:
     - Evidence file(s).
     - Case identifier and descriptive metadata.
     - Optional tags or classification labels (e.g., “confidential”, “PII”).

2. **Upload and Hashing (Frontend → Backend)**
   - The frontend sends the file (over HTTPS) to the FastAPI backend along with metadata.
   - The backend:
     - Streams the file to temporary storage.
     - Computes a **SHA‑256 hash** of the file contents.
     - Optionally computes a hash of structured metadata for on‑chain storage.

3. **Encryption and Off‑Chain Storage**
   - The backend generates or retrieves an appropriate AES encryption key (from a KMS or secure key store).
   - The evidence file is encrypted using AES (e.g., AES‑256‑GCM).
   - The encrypted file is stored in the off‑chain evidence storage (e.g., `evidence-bucket/case-123/evidence-abc.enc`).
   - The backend records the storage location reference (not the raw file) in PostgreSQL.

4. **Metadata Persistence (Backend → PostgreSQL)**
   - The backend creates an evidence record in PostgreSQL containing:
     - Internal evidence ID.
     - Case ID and descriptive metadata.
     - File hash (SHA‑256).
     - Metadata hash (if applicable).
     - Off‑chain storage URI/path.
     - Current status (e.g., `REGISTERED`).
   - The initial **custody event** (“COLLECTED” or “REGISTERED”) is prepared.

5. **Blockchain Transaction (Backend → Ethereum)**
   - The backend constructs a transaction to the **Evidence Custody Smart Contract** that includes:
     - Evidence ID (or derived on‑chain identifier).
     - SHA‑256 hash of the evidence file.
     - Optional metadata hash.
     - Initial custody event details (actor ID pseudonym, action type, timestamp).
   - The transaction is signed using the backend’s configured Ethereum account or via a signing service.
   - The transaction is sent to the Ethereum network (Ganache in development).
   - Upon confirmation, the transaction hash and on‑chain event identifiers are returned.

6. **Post‑Transaction Updates (Backend → PostgreSQL & Frontend)**
   - The backend stores the transaction hash and block number for the evidence registration and initial custody event in PostgreSQL.
   - The frontend receives a confirmation that:
     - Evidence has been successfully stored off‑chain.
     - A corresponding immutable blockchain record has been created.
   - The UI updates the case view and custody timeline.

Subsequent actions such as **view**, **transfer**, and **verify** follow a similar pattern: the backend records the action in PostgreSQL and appends a corresponding custody event to the blockchain.

---

## Trust Boundaries

The system introduces several important trust boundaries:

- **User Device ↔ Frontend**
  - Transport: HTTPS.
  - Trust assumptions:
    - The user’s browser environment may be untrusted (malware, keyloggers).
    - The system relies on robust authentication (e.g., MFA) and session handling.
  - Controls:
    - TLS everywhere.
    - Strong authentication and authorization.
    - CSRF and XSS protections at the UI and API levels.

- **Frontend ↔ Backend API**
  - Transport: HTTPS between the React frontend and FastAPI backend.
  - Trust assumptions:
    - Backend is trusted to enforce access control and process business logic.
  - Controls:
    - Token‑based authentication (e.g., JWT or opaque tokens).
    - Role‑based access control (RBAC) and granular permissions for custody actions.

- **Backend API ↔ Database (PostgreSQL)**
  - Private network segment or container network.
  - Trust assumptions:
    - Database should not be directly reachable from the internet.
    - Backend is responsible for query hygiene and input validation.
  - Controls:
    - Network‑level isolation and firewall rules.
    - Encrypted connections (TLS) to the database where supported.
    - Principle of least privilege for DB credentials.

- **Backend API ↔ Off‑Chain Evidence Storage**
  - Communication with storage services (e.g., S3 endpoint or on‑prem file store) over private or encrypted channels.
  - Trust assumptions:
    - Storage infrastructure may be considered semi‑trusted; data must be encrypted at rest.
  - Controls:
    - Strong encryption (AES) with keys not accessible to storage admins.
    - Integrity protection via SHA‑256 hashes stored on‑chain.
    - Access policies limiting who/what can read encrypted evidence.

- **Backend API ↔ Blockchain Network (Ethereum)**
  - Backend connects to an Ethereum node (local Ganache or remote RPC endpoint).
  - Trust assumptions:
    - The consensus rules of the blockchain ensure immutability of confirmed transactions.
    - The smart contract code is publicly verifiable.
  - Controls:
    - Contract access control for who can register evidence or create custody events.
    - Use of permissioned networks for sensitive deployments.
    - Monitoring for unexpected contract activity.

---

## Rationale for Off‑Chain Evidence Storage

Evidence files are **intentionally stored off‑chain** for the following reasons:

- **Scalability and Size Constraints**
  - Digital evidence (disk images, memory dumps, video, logs) can be extremely large (GB–TB).
  - Storing such data directly on Ethereum is economically and technically infeasible due to gas costs and block size limits.

- **Performance**
  - Accessing large files on‑chain would be slow and impractical.
  - Off‑chain storage optimized for large objects (e.g., object stores, NAS) provides better throughput and latency.

- **Privacy and Legal Requirements**
  - Evidence often contains sensitive or personally identifiable information (PII).
  - Keeping raw data off‑chain allows compliance with data protection regulations (e.g., retention policies, right to erasure) while still preserving cryptographic integrity guarantees via hashes.

- **Security and Key Management**
  - Off‑chain, encrypted storage enables flexible encryption strategies, key rotation, and granular access control.
  - Compromise of blockchain data does not expose raw evidence, since only hashes and metadata are on‑chain.

- **Immutability Where It Matters Most**
  - The **integrity proof** (SHA‑256 hash) and **custody events** are stored on‑chain, providing strong guarantees against tampering.
  - If the off‑chain evidence is altered, the hash comparison against the on‑chain record will fail, making tampering immediately detectable.

This hybrid architecture balances the immutability and transparency of blockchain with the scalability, privacy, and performance characteristics of traditional storage systems.

