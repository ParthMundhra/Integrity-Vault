## Blockchain Layer (`blockchain/`)

The blockchain layer contains the **Ethereum smart contracts** and deployment tooling used to provide an immutable record of evidence registration and chain‑of‑custody events.

### Purpose of the Smart Contract

The primary contract, `contracts/EvidenceCustody.sol`, is responsible for:

- **Evidence registration**
  - Storing a canonical identifier for each piece of evidence.
  - Recording the **SHA‑256 hash** of the off‑chain evidence file.
  - Optionally storing a hash of structured case metadata.
- **Custody event logging**
  - Appending a chronological sequence of custody events for each evidence ID.
  - Ensuring that once recorded, events cannot be altered or deleted.

### Custody Events

Custody events capture key actions in the evidence lifecycle, such as:

- `COLLECTED`, `REGISTERED`, `TRANSFERRED`, `VIEWED`, `VERIFIED`, `RELEASED`.
- Who performed the action, when, and between which custodians (where applicable).
- High‑level location/context and optional hashes of off‑chain reports or notes.

These events form an **immutable, auditable timeline** that supports legal and internal investigation requirements.

### How Hashes Are Stored On‑Chain

- The backend computes **SHA‑256** hashes of evidence files and metadata.
- Those hashes are passed to the `EvidenceCustody` contract:
  - `evidenceHash` – hash of the evidence content.
  - `metadataHash` – hash of associated metadata (optional).
- Hashes are stored in contract storage and emitted in events so that:
  - Any later copy of the evidence can be recomputed and compared.
  - Tampering with off‑chain evidence becomes detectable.

### Ganache for Local Development

During development, the project uses **Ganache** (or a similar local Ethereum node) to:

- Provide a fast, disposable blockchain for testing contract behavior.
- Allow developers to deploy `EvidenceCustody` using accounts with test ETH.
- Exercise end‑to‑end flows:
  - Backend → contract (evidence registration & custody events).
  - Frontend → blockchain (read‑only queries and timeline views).

The `scripts/deploy.js` file is a **placeholder** deployment script that will be extended to use a tool like **Hardhat** or **Truffle** to compile and deploy the contract to Ganache or other Ethereum networks.
