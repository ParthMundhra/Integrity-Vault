## Frontend (`frontend/`)

The frontend is a **React (Vite)** application that provides the investigator and auditor dashboard for the Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System.

Its key responsibilities are:

- Presenting intuitive workflows for evidence upload and registration.
- Visualizing custody timelines and blockchain-backed integrity information.
- Guiding users through verification flows while hiding underlying complexity.

### Structure

- `src/components/Navbar.jsx`
  - Shared navigation bar across pages.
  - In a full implementation this will integrate with routing and authentication.

- `src/pages/UploadEvidence.jsx`
  - Upload form for new digital evidence.
  - Captures case metadata and evidence files.
  - Will call the backend `POST /api/evidence/upload` endpoint and display hashing/encryption progress.

- `src/pages/EvidenceTimeline.jsx`
  - Timeline view of custody events for a selected evidence item.
  - Will query the backend (and indirectly the blockchain) for a sequence of custody events and render them chronologically.

- `src/pages/VerifyEvidence.jsx`
  - Integrity verification workflow.
  - Allows users to verify a stored or locally provided evidence file against the canonical hash recorded by the backend and smart contract.

The frontend is intentionally minimal at this stage, providing skeleton components that can be wired up to the API and smart contracts as the project evolves.
