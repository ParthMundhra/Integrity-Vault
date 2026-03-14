## Smart Contract Design

This document describes the conceptual design of the **Evidence Custody Smart Contract** used in the Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System.

The purpose of the contract is to provide an **immutable, verifiable, and auditable** record of:

- Evidence registration.
- Custody events over time (collect, transfer, view, verify, release, etc.).

No Solidity code is provided here; instead, this is a logic‑level specification intended to guide later implementation.

---

## Contract Purpose and Scope

The smart contract is responsible for:

- Recording the **existence** of evidence items via their cryptographic hashes.
- Recording a sequence of **custody events** for each evidence item.
- Enforcing **basic invariants**, such as:
  - Evidence cannot be re‑registered with conflicting hashes.
  - Custody events are appended in order and associated with existing evidence.
- Exposing read‑only query functions to reconstruct the custody timeline for any evidence item.

The smart contract is **not** responsible for:

- Storing raw evidence data (this remains off‑chain).
- Implementing full user authentication or complex authorization logic (handled primarily in the backend).
- Handling encryption keys or decryption operations.

---

## Data Model

### Evidence Identifier

Each piece of evidence is assigned a canonical **Evidence ID** by the backend. On‑chain, this may be represented as:

- A `bytes32` identifier (e.g., hash of a backend UUID or composite key), or
- A `uint256` auto‑incremented ID managed by the contract.

The design should allow:

- Unique identification of each evidence record.
- Efficient lookup of associated custody events.

### Evidence Registration Record

For each evidence item, the contract stores:

- **evidenceId**: Unique identifier for the evidence item.
- **evidenceHash**: SHA‑256 hash of the evidence file (or a standardized representation of it).
- **metadataHash** (optional): Hash of case metadata or a structured JSON representation.
- **registeredBy**: Address (or role identifier) of the entity that registered the evidence.
- **registeredAt**: Block timestamp when the evidence was registered.
- **status**: Simple lifecycle status (e.g., `ACTIVE`, `RETIRED`) if exposed.

These fields provide a minimal yet sufficient record for verifying that:

- A particular evidence item existed at or before the registration timestamp.
- The contents of the evidence have not changed since registration, as long as SHA‑256 remains secure.

### CustodyEvent Structure

Custody events represent actions taken upon evidence over time. A conceptual `CustodyEvent` structure includes:

- **eventId**: Sequential identifier (per evidence) or a global event index.
- **evidenceId**: The associated evidence identifier.
- **actionType**: Enumerated value describing the action, for example:
  - `COLLECTED`
  - `REGISTERED`
  - `TRANSFERRED`
  - `VIEWED`
  - `VERIFIED`
  - `RELEASED`
- **performedBy**: Address (or pseudonymous ID) of the actor responsible for the action.
- **fromParty** (optional): Previous custodian (for transfer events).
- **toParty** (optional): New custodian (for transfer events).
- **location** (optional): High‑level location or organizational unit (e.g., lab, department).
- **timestamp**: Block timestamp when the event was recorded.
- **notesHash** (optional): Hash of off‑chain notes or justification documents.

Events are stored in a way that allows:

- Efficient retrieval of all events for a given `evidenceId`.
- Verification of chronological order and completeness.

---

## Evidence Registration Logic

### Preconditions

When the backend initiates evidence registration, the contract should enforce the following conditions:

- The `evidenceId` is not already registered (or, if it is, the contract logic must ensure that hashes are consistent and that multiple registrations are intentional and auditable).
- The provided `evidenceHash` is non‑zero and well‑formed.
- The caller (backend‑controlled address or authorized role) is permitted to perform registrations.

### Registration Steps

1. **Input Validation**
   - Check that `evidenceId` is not yet associated with a conflicting `evidenceHash`.
   - Reject calls with zero or invalid hashes.

2. **State Update**
   - Create or update the evidence registration record:
     - Set `evidenceHash`, `metadataHash` (if provided).
     - Set `registeredBy` to `msg.sender` or another appropriate identifier.
     - Set `registeredAt` to the current block timestamp.
   - Initialize any necessary counters for custody events (e.g., starting `eventId` at 0 or 1).

3. **Emit Registration Event**
   - Emit an `EvidenceRegistered` event containing:
     - `evidenceId`
     - `evidenceHash`
     - `metadataHash` (if any)
     - `registeredBy`
     - `timestamp`

This event is part of the immutable on‑chain log and provides an auditable record of the initial evidence registration.

---

## Custody Actions

Custody actions represent transitions in who has responsibility or access to the evidence, or significant interactions with it (such as viewing or verifying).

### General Design Considerations

- **Append‑Only Model**:
  - The contract allows only appending new custody events.
  - Existing events are never modified or deleted.
- **Monotonic Event Ordering**:
  - For each `evidenceId`, custody events should have strictly increasing `eventId`s or rely on natural block log ordering.
- **Authorization**:
  - The contract trusts the backend to enforce fine‑grained authorization.
  - On‑chain, only a limited set of addresses (e.g., backend services or multisig wallets) may be allowed to submit custody events.

### Custody Event Types

#### 1. Collection / Initial Registration Event

- Typically occurs together with or immediately after evidence registration.
- Represents the first custodial control of the evidence.
- Fields:
  - `actionType = COLLECTED` or `REGISTERED`
  - `performedBy` = address responsible for collection.
  - `toParty` = initial custodian (may be the same as `performedBy`).

#### 2. Transfer of Custody

- Represents a handover of physical or logical control of the evidence.
- Examples: Investigator → Lab Technician, Lab → Secure Archive.
- Fields:
  - `actionType = TRANSFERRED`
  - `fromParty` = current custodian.
  - `toParty` = new custodian.
  - `performedBy` = address that initiated/approved the transfer (may be one of the parties or a supervisor).
  - `location` = destination or context (optional, coarse‑grained).

Contract logic should:

- Verify that the evidence is registered.
- Optionally verify that `fromParty` matches the last known custodian (if this state is tracked on‑chain).
- Append the event and update any stored “current custodian” field.

#### 3. Viewing / Access

- Represents significant access to the evidence (e.g., viewing decrypted contents, downloading a copy).
- Fields:
  - `actionType = VIEWED`
  - `performedBy` = user that accessed the evidence.
  - `location` = workstation, lab, or logical environment (optional, coarse‑grained).

Depending on privacy requirements, frequent low‑level views may be aggregated off‑chain and only major events recorded on‑chain.

#### 4. Integrity Verification

- Represents an explicit check that the off‑chain evidence file still matches the on‑chain hash.
- Fields:
  - `actionType = VERIFIED`
  - `performedBy` = user or automated process that performed the verification.
  - `notesHash` = hash of verification report or log.

The backend performs the actual hash comparison and records a summary result on‑chain.

#### 5. Release / Final Disposition

- Represents the final disposition of evidence (e.g., returned, destroyed, or archived).
- Fields:
  - `actionType = RELEASED`
  - `performedBy` = user authorizing release.
  - `toParty` = final recipient or destination (if applicable).

---

## Events and Query Functions

### On‑Chain Events

The contract should emit events that external systems can subscribe to, such as:

- `EvidenceRegistered(evidenceId, evidenceHash, metadataHash, registeredBy, timestamp)`
- `CustodyEventAppended(evidenceId, eventId, actionType, performedBy, fromParty, toParty, location, timestamp, notesHash)`

These events allow:

- Off‑chain indexing by log aggregators or analytics systems.
- Near real‑time updates in the frontend when new custody actions occur.

### Read‑Only Queries

The contract should provide functions to:

- Fetch core evidence registration data by `evidenceId`.
- Retrieve:
  - The total number of custody events for a given `evidenceId`.
  - A specific custody event by `evidenceId` and `eventId`.
  - Optionally, the current custodian of a given evidence item.

These queries enable the frontend and backend to reconstruct a complete custody timeline for display and for verification workflows.

---

## Security and Integrity Considerations

- **Immutability**:
  - Once registered, evidence hashes and custody events must not be modifiable.
  - Any attempt to “correct” a record should be represented as an additional event, not a modification.

- **Minimal On‑Chain Data**:
  - To preserve privacy and reduce gas costs, only necessary data (hashes, IDs, and high‑level context) should be stored on‑chain.
  - Detailed descriptions, notes, and PII‑rich information remain off‑chain and referenced by hashes.

- **Access Control**:
  - Only designated accounts (e.g., backend service accounts, multisig administrators) may call functions that modify state.
  - User‑level authorization is primarily enforced by the backend before transactions are constructed.

- **Upgradability and Governance**:
  - If the design includes upgradability, it should be carefully controlled:
    - Governance by multi‑party approval (e.g., multi‑sig).
    - Clear migration paths that preserve the integrity of historical records.

This design aims to provide a clear separation of responsibilities: off‑chain systems manage large, encrypted evidence files and rich metadata, while the smart contract provides a minimal, tamper‑evident ledger of evidence existence and custody history.

