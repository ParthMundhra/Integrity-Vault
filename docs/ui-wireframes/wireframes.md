## UI Wireframes

This document describes the core UI screens for the **Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System** and provides simple ASCII wireframes.

The initial release focuses on three primary workflows:

- Evidence upload and registration.
- Viewing the custody timeline for an evidence item.
- Verifying the integrity of evidence against blockchain records.

The actual implementation will use a modern React (Vite) frontend with a clean, accessible design. These wireframes are conceptual and omit styling details.

---

## Global Layout Concepts

- **Top Navigation Bar**
  - Product name / logo.
  - Navigation links: `Dashboard`, `Evidence`, `Cases`, `Verification`, `Admin`.
  - User menu with profile, role, and logout.

- **Left Sidebar (Optional)**
  - Case filter, evidence search, and quick links.

- **Main Content Area**
  - Page‑specific content (forms, tables, timelines).

---

## Evidence Upload Page

**Purpose**: Allow authorized users to upload new digital evidence, capture metadata, and initiate blockchain registration.

Key elements:

- Case selection and high‑level metadata.
- File upload area with drag‑and‑drop.
- Hashing and encryption status indicators.
- Confirmation and summary before submission.

**ASCII Wireframe**

```text
+----------------------------------------------------------------------------------+
| [Logo] Blockchain Forensics                        User: Alice (Investigator)   |
|----------------------------------------------------------------------------------|
| Dashboard | Evidence | Cases | Verification | Admin                             |
|----------------------------------------------------------------------------------|
| Evidence > New Upload                                                              |
|----------------------------------------------------------------------------------|
| Case Information                                                                  |
| -------------------------------------------------------------------------------- |
| Case ID:           [______________]  [Search]                                    |
| Case Name:         [______________________________________________]             |
| Description:       [______________________________________________]             |
|                    [______________________________________________]             |
| Tags:              [ + Add Tag ]                                                 |
|----------------------------------------------------------------------------------|
| Evidence File                                                                      |
| -------------------------------------------------------------------------------- |
| [ Drag & Drop files here ]                                                        |
| [ Browse... ]                                                                     |
|                                                                                   |
| File Name:         evidence-image.E01                                            |
| Size:              14.2 GB                                                       |
| Hash (SHA-256):    [computing...]  [■□□□□ 12%]                                   |
| Encryption:        [pending]                                                     |
|----------------------------------------------------------------------------------|
| Advanced Options (collapse/expand)                                               |
| - Retention Policy: [Standard ▼]                                                 |
| - Classification:   [Confidential ▼]                                             |
|----------------------------------------------------------------------------------|
| [ Cancel ]                                              [ Register Evidence ]    |
+----------------------------------------------------------------------------------+
```

Interaction notes:

- After file selection, the UI shows a progress bar while hashing is performed (client‑side, server‑side, or both).
- Once hashing and upload complete, the **Register Evidence** button becomes enabled.
- Upon submission, the UI transitions to a confirmation view showing the evidence ID and blockchain transaction reference (once available).

---

## Custody Timeline Page

**Purpose**: Provide a clear, chronological view of all custody events for a given evidence item, including who handled it, when, and where.

Key elements:

- Evidence summary panel.
- Chronological list or timeline of events.
- Indicators for key event types (collection, transfer, verification, release).

**ASCII Wireframe**

```text
+----------------------------------------------------------------------------------+
| [Logo] Blockchain Forensics                        User: Bob (Auditor)          |
|----------------------------------------------------------------------------------|
| Dashboard | Evidence | Cases | Verification | Admin                             |
|----------------------------------------------------------------------------------|
| Evidence > EV-2026-001 > Custody Timeline                                        |
|----------------------------------------------------------------------------------|
| Evidence Summary                                                                  |
| -------------------------------------------------------------------------------- |
| Evidence ID:      EV-2026-001                                                    |
| Case ID:          CASE-123                                                       |
| Description:      Disk image from workstation WKS-01                             |
| Hash (SHA-256):   8f2a...c91b                                                   |
| On-chain Status:  Registered (Tx: 0xabc...123)                                   |
| Current Custodian: Lab - Digital Forensics Unit                                  |
|----------------------------------------------------------------------------------|
| Custody Timeline                                                                  |
| -------------------------------------------------------------------------------- |
|  [2026-03-10 09:15]  COLLECTED                                                   |
|    - By: Alice (Investigator)                                                    |
|    - Location: Field                                                             |
|                                                                                   |
|  [2026-03-10 10:30]  REGISTERED                                                  |
|    - By: Alice (Investigator)                                                    |
|    - On-chain Tx: 0xabc...123                                                    |
|                                                                                   |
|  [2026-03-11 08:00]  TRANSFERRED                                                 |
|    - From: Alice (Investigator)                                                  |
|    - To:   David (Lab Technician)                                                |
|    - Location: Forensics Lab                                                     |
|                                                                                   |
|  [2026-03-11 09:45]  VIEWED                                                      |
|    - By: David (Lab Technician)                                                  |
|    - Location: Lab Workstation 3                                                 |
|                                                                                   |
|  [2026-03-12 16:20]  VERIFIED                                                    |
|    - By: Bob (Auditor)                                                           |
|    - Result: MATCH (hash consistent with blockchain)                             |
|    - Verification Report: [Download]                                             |
|----------------------------------------------------------------------------------|
| [ Back to Evidence List ]                                                        |
+----------------------------------------------------------------------------------+
```

Interaction notes:

- Timeline may support filtering by event type and date range.
- Clicking an event may reveal more details (e.g., notes, associated documentation).
- The UI may highlight verification failures or missing events in red.

---

## Integrity Verification Page

**Purpose**: Allow users (typically auditors or supervisors) to verify that an off‑chain evidence file still matches the on‑chain hash and to view the verification result.

Key elements:

- Selection of evidence to verify (by ID, case, or search).
- Summary of on‑chain hash and metadata.
- Input field or file selection for the local evidence copy, if applicable.
- Clear display of verification status.

**ASCII Wireframe**

```text
+----------------------------------------------------------------------------------+
| [Logo] Blockchain Forensics                        User: Bob (Auditor)          |
|----------------------------------------------------------------------------------|
| Dashboard | Evidence | Cases | Verification | Admin                             |
|----------------------------------------------------------------------------------|
| Verification                                                                      |
|----------------------------------------------------------------------------------|
| Select Evidence                                                                   |
| -------------------------------------------------------------------------------- |
| Search: [ EV-2026-001          ] [Search]                                        |
|                                                                                   |
| Evidence ID:      EV-2026-001                                                    |
| Case ID:          CASE-123                                                       |
| Description:      Disk image from workstation WKS-01                             |
| On-chain Hash:    8f2a...c91b                                                   |
| Last Verified:    2026-03-12 16:20 (MATCH)                                       |
|----------------------------------------------------------------------------------|
| Verification Input                                                                |
| -------------------------------------------------------------------------------- |
| [ Option A ] Use stored encrypted copy                                           |
|    - Backend will retrieve, decrypt, and hash the current stored file.          |
|                                                                                   |
| [ Option B ] Upload file to compare                                              |
|    - [ Drag & Drop local copy here ]                                            |
|    - [ Browse... ]                                                              |
|                                                                                   |
| Progress: [■■■■■□□□□□] 54%                                                       |
| Current Hash:    computing...                                                    |
|----------------------------------------------------------------------------------|
| Verification Result                                                               |
| -------------------------------------------------------------------------------- |
| Status: [ MATCH ]                                                                |
| Details:                                                                          |
|   - On-chain Hash: 8f2a...c91b                                                  |
|   - Computed Hash: 8f2a...c91b                                                  |
|   - Block Number:  123456                                                       |
|   - Tx Hash:       0xabc...123                                                  |
|                                                                                   |
| [ Export Verification Report ]   [ Record Verification Event On-Chain ]          |
|----------------------------------------------------------------------------------|
| [ Back to Dashboard ]                                                            |
+----------------------------------------------------------------------------------+
```

Interaction notes:

- Users can choose to verify against the stored encrypted copy (server‑side process) or provide their own copy of the evidence file.
- Upon successful verification, the user may optionally record a **VERIFIED** custody event on‑chain, with a reference to a verification report stored off‑chain.

---

## Future Enhancements

- Role‑specific dashboards (investigators vs. lab technicians vs. auditors).
- Case overview pages with aggregated evidence status indicators.
- Dark mode and accessibility enhancements (e.g., keyboard navigation, screen reader support).
- Integration with SSO/IdP for enterprise deployments.

These wireframes provide a starting point for implementing a user‑friendly, security‑focused UI in React.

