## Documentation (`docs/`)

The `docs/` directory contains architecture and security documentation for the Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System. It is organized by topic so that engineers, security reviewers, and stakeholders can quickly find relevant information.

### Structure

- `architecture/`
  - `system-architecture.md` – High‑level overview of system components, data flows from evidence collection to blockchain recording, trust boundaries, and the rationale for off‑chain evidence storage.

- `threat-model/`
  - `threat-model.md` – Assets, threat actors, key threats (e.g., evidence tampering, insider modification, forged custody events, unauthorized access), and mitigations for each.

- `smart-contract/`
  - `contract-design.md` – Conceptual design of the Ethereum smart contract used for evidence registration and custody events, including the `CustodyEvent` structure and on‑chain data model.

- `ui-wireframes/`
  - `wireframes.md` – ASCII wireframes and descriptions of the main UI screens, including the evidence upload page, custody timeline page, and integrity verification page.

- `decisions/`
  - `adr-001-offchain-storage.md` – Architecture Decision Record explaining why raw evidence is stored off‑chain with only hashes and custody events on‑chain, including trade‑offs and alternatives considered.

### Usage

- **Engineers** should consult `architecture/` and `smart-contract/` when implementing or modifying backend, blockchain, and frontend components.
- **Security and compliance teams** should reference `threat-model/` and `decisions/` for risk assessments and audits.
- **Product and UX** teams can use `ui-wireframes/` as a starting point for high‑fidelity designs.

All new significant architectural or security decisions should be documented here, ideally as additional ADRs under `docs/decisions/`.
