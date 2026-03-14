import React from "react";
import { Navbar } from "../components/Navbar";

/**
 * VerifyEvidence
 *
 * Placeholder page for verifying the integrity of an evidence file
 * against the canonical hash stored by the backend / blockchain.
 */
export function VerifyEvidence() {
  return (
    <div>
      <Navbar />
      <main style={{ padding: "1.5rem", maxWidth: "960px", margin: "0 auto" }}>
        <h1>Verify Evidence Integrity</h1>
        <p style={{ marginTop: "0.5rem", color: "#4b5563" }}>
          Compare a local or stored copy of evidence against its blockchain-backed
          hash.
        </p>

        <section
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            border: "1px solid #e5e7eb",
            borderRadius: "0.5rem",
          }}
        >
          <h2>Select Evidence</h2>
          <div
            style={{
              marginTop: "0.75rem",
              display: "flex",
              gap: "0.75rem",
              alignItems: "center",
            }}
          >
            <input
              type="text"
              placeholder="Evidence ID (e.g., EV-2026-001)"
              style={{ flex: 1 }}
            />
            <button type="button">Load</button>
          </div>
          <p style={{ marginTop: "0.5rem", fontSize: "0.85rem", color: "#6b7280" }}>
            In the full implementation this will fetch on-chain hash and metadata
            for the specified evidence ID.
          </p>
        </section>

        <section
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            border: "1px solid #e5e7eb",
            borderRadius: "0.5rem",
          }}
        >
          <h2>Verification Input</h2>
          <div style={{ marginTop: "0.75rem" }}>
            <p style={{ fontWeight: 600 }}>Option A: Use stored encrypted copy</p>
            <p style={{ fontSize: "0.85rem", color: "#6b7280" }}>
              Backend will retrieve, decrypt, and hash the evidence stored in the
              secure evidence repository.
            </p>
          </div>
          <div style={{ marginTop: "1rem" }}>
            <p style={{ fontWeight: 600 }}>Option B: Upload file to compare</p>
            <div
              style={{
                marginTop: "0.5rem",
                padding: "1.5rem",
                border: "1px dashed #9ca3af",
                borderRadius: "0.5rem",
                textAlign: "center",
                color: "#6b7280",
              }}
            >
              Drag &amp; drop local evidence file here, or click to browse.
            </div>
          </div>
        </section>

        <section
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            border: "1px solid #e5e7eb",
            borderRadius: "0.5rem",
          }}
        >
          <h2>Verification Result</h2>
          <p style={{ marginTop: "0.75rem", fontSize: "0.9rem" }}>
            Status: <strong>PENDING</strong>
          </p>
          <p style={{ fontSize: "0.85rem", color: "#6b7280" }}>
            Once connected to the backend, this section will display whether the
            computed hash matches the on-chain hash, along with relevant
            transaction and block details.
          </p>
        </section>
      </main>
    </div>
  );
}

