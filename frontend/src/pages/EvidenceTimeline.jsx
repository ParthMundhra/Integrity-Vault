import React from "react";
import { Navbar } from "../components/Navbar";

/**
 * EvidenceTimeline
 *
 * Placeholder page for visualizing the custody timeline of a single
 * evidence item. This will eventually query the backend and blockchain
 * for custody events and render them as a chronological list or timeline.
 */
export function EvidenceTimeline() {
  const mockEvents = [
    {
      timestamp: "2026-03-10 09:15",
      type: "COLLECTED",
      actor: "Alice (Investigator)",
      location: "Field",
    },
    {
      timestamp: "2026-03-10 10:30",
      type: "REGISTERED",
      actor: "Alice (Investigator)",
      location: "Backend / Blockchain",
    },
    {
      timestamp: "2026-03-11 08:00",
      type: "TRANSFERRED",
      actor: "Alice → David",
      location: "Forensics Lab",
    },
  ];

  return (
    <div>
      <Navbar />
      <main style={{ padding: "1.5rem", maxWidth: "960px", margin: "0 auto" }}>
        <h1>Evidence Custody Timeline</h1>
        <p style={{ marginTop: "0.5rem", color: "#4b5563" }}>
          Review the immutable chain-of-custody for a specific evidence item.
        </p>

        <section
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            border: "1px solid #e5e7eb",
            borderRadius: "0.5rem",
          }}
        >
          <h2>Evidence Summary</h2>
          <p style={{ marginTop: "0.75rem", fontSize: "0.9rem" }}>
            <strong>Evidence ID:</strong> EV-2026-001
            <br />
            <strong>Case ID:</strong> CASE-123
            <br />
            <strong>Description:</strong> Disk image from workstation WKS-01
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
          <h2>Custody Events</h2>
          <ul style={{ listStyle: "none", padding: 0, marginTop: "1rem" }}>
            {mockEvents.map((evt, idx) => (
              <li
                key={idx}
                style={{
                  padding: "0.75rem 0",
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                <div style={{ fontWeight: 600 }}>
                  [{evt.timestamp}] {evt.type}
                </div>
                <div style={{ fontSize: "0.9rem", color: "#4b5563" }}>
                  By: {evt.actor} | Location: {evt.location}
                </div>
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}

