import React from "react";

/**
 * Simple top navigation bar for the investigator dashboard.
 *
 * In a production UI this will be styled and integrated with routing and
 * authentication state.
 */
export function Navbar() {
  return (
    <nav
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0.75rem 1.5rem",
        borderBottom: "1px solid #e5e7eb",
      }}
    >
      <div style={{ fontWeight: 600 }}>
        Blockchain Forensics &amp; Chain-of-Custody
      </div>
      <div style={{ display: "flex", gap: "1rem", fontSize: "0.9rem" }}>
        <span>Dashboard</span>
        <span>Evidence</span>
        <span>Cases</span>
        <span>Verification</span>
      </div>
      <div style={{ fontSize: "0.85rem", color: "#4b5563" }}>User</div>
    </nav>
  );
}

