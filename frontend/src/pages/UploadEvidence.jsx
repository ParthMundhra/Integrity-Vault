import React from "react";
import { Navbar } from "../components/Navbar";

/**
 * UploadEvidence
 *
 * Placeholder page for uploading and registering new digital evidence.
 * This will eventually integrate with the FastAPI backend's /evidence/upload
 * endpoint and show hashing/encryption progress.
 */
export function UploadEvidence() {
  return (
    <div>
      <Navbar />
      <main style={{ padding: "1.5rem", maxWidth: "960px", margin: "0 auto" }}>
        <h1>Upload Evidence</h1>
        <p style={{ marginTop: "0.5rem", color: "#4b5563" }}>
          Upload new digital evidence, capture case metadata, and initiate
          blockchain-backed registration.
        </p>

        <section
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            border: "1px solid #e5e7eb",
            borderRadius: "0.5rem",
          }}
        >
          <h2>Case Information</h2>
          <div style={{ marginTop: "0.75rem", display: "grid", gap: "0.75rem" }}>
            <label>
              Case ID
              <input
                type="text"
                placeholder="e.g., CASE-2026-001"
                style={{ display: "block", width: "100%", marginTop: "0.25rem" }}
              />
            </label>
            <label>
              Description
              <textarea
                placeholder="Brief description of the evidence source and context."
                rows={3}
                style={{ display: "block", width: "100%", marginTop: "0.25rem" }}
              />
            </label>
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
          <h2>Evidence File</h2>
          <div
            style={{
              marginTop: "0.75rem",
              padding: "1.5rem",
              border: "1px dashed #9ca3af",
              borderRadius: "0.5rem",
              textAlign: "center",
              color: "#6b7280",
            }}
          >
            Drag &amp; drop evidence file here, or click to browse.
          </div>
          <p style={{ marginTop: "0.75rem", fontSize: "0.85rem" }}>
            Hashing and encryption progress will be displayed here once the
            backend integration is implemented.
          </p>
        </section>

        <div
          style={{
            marginTop: "1.5rem",
            display: "flex",
            justifyContent: "flex-end",
            gap: "0.75rem",
          }}
        >
          <button type="button">Cancel</button>
          <button type="button" style={{ fontWeight: 600 }}>
            Register Evidence
          </button>
        </div>
      </main>
    </div>
  );
}

