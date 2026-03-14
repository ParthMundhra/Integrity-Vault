// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title EvidenceCustody
 * @notice Smart contract for registering digital evidence and recording
 *         an immutable chain-of-custody.
 *
 * This contract intentionally stores only identifiers, hashes, and
 * high-level custody metadata. Raw evidence remains encrypted off-chain.
 */
contract EvidenceCustody {
    struct Evidence {
        bool exists;
        bytes32 evidenceHash; // SHA-256 hash of evidence bytes (standardized off-chain)
        bytes32 metadataHash; // Optional hash of structured metadata
        address registeredBy;
        uint256 registeredAt;
    }

    enum ActionType {
        COLLECTED,
        REGISTERED,
        TRANSFERRED,
        VIEWED,
        VERIFIED,
        RELEASED
    }

    struct CustodyEvent {
        uint256 eventId;
        bytes32 evidenceId;
        ActionType actionType;
        address performedBy;
        address fromParty;
        address toParty;
        string location;
        uint256 timestamp;
        bytes32 notesHash; // Optional hash of off-chain notes/reports
    }

    // Evidence ID (bytes32) to registration record.
    mapping(bytes32 => Evidence) private evidences;

    // Evidence ID to list of custody events.
    mapping(bytes32 => CustodyEvent[]) private custodyEvents;

    event EvidenceRegistered(
        bytes32 indexed evidenceId,
        bytes32 evidenceHash,
        bytes32 metadataHash,
        address indexed registeredBy,
        uint256 registeredAt
    );

    event CustodyEventAppended(
        bytes32 indexed evidenceId,
        uint256 indexed eventId,
        ActionType actionType,
        address indexed performedBy,
        address fromParty,
        address toParty,
        string location,
        uint256 timestamp,
        bytes32 notesHash
    );

    /**
     * @notice Register a new piece of evidence.
     * @param evidenceId Canonical identifier for the evidence (bytes32).
     * @param evidenceHash SHA-256 hash of the evidence file, computed off-chain.
     * @param metadataHash Optional hash of structured metadata.
     */
    function registerEvidence(
        bytes32 evidenceId,
        bytes32 evidenceHash,
        bytes32 metadataHash
    ) external {
        require(evidenceId != bytes32(0), "invalid evidenceId");
        require(evidenceHash != bytes32(0), "invalid evidenceHash");
        require(!evidences[evidenceId].exists, "evidence already registered");

        evidences[evidenceId] = Evidence({
            exists: true,
            evidenceHash: evidenceHash,
            metadataHash: metadataHash,
            registeredBy: msg.sender,
            registeredAt: block.timestamp
        });

        emit EvidenceRegistered(
            evidenceId,
            evidenceHash,
            metadataHash,
            msg.sender,
            block.timestamp
        );

        // Optionally, an initial custody event can be appended off-chain
        // via a separate call to `appendCustodyEvent`.
    }

    /**
     * @notice Append a custody event for an existing evidence record.
     * @dev The backend is expected to enforce fine-grained authorization.
     */
    function appendCustodyEvent(
        bytes32 evidenceId,
        ActionType actionType,
        address fromParty,
        address toParty,
        string calldata location,
        bytes32 notesHash
    ) external {
        require(evidences[evidenceId].exists, "evidence not registered");

        uint256 eventId = custodyEvents[evidenceId].length;

        CustodyEvent memory evt = CustodyEvent({
            eventId: eventId,
            evidenceId: evidenceId,
            actionType: actionType,
            performedBy: msg.sender,
            fromParty: fromParty,
            toParty: toParty,
            location: location,
            timestamp: block.timestamp,
            notesHash: notesHash
        });

        custodyEvents[evidenceId].push(evt);

        emit CustodyEventAppended(
            evidenceId,
            eventId,
            actionType,
            msg.sender,
            fromParty,
            toParty,
            location,
            block.timestamp,
            notesHash
        );
    }

    // -------------------------
    // Read-only helper methods
    // -------------------------

    function getEvidence(bytes32 evidenceId)
        external
        view
        returns (Evidence memory)
    {
        require(evidences[evidenceId].exists, "evidence not registered");
        return evidences[evidenceId];
    }

    function getCustodyEventCount(bytes32 evidenceId)
        external
        view
        returns (uint256)
    {
        return custodyEvents[evidenceId].length;
    }

    function getCustodyEvent(bytes32 evidenceId, uint256 eventId)
        external
        view
        returns (CustodyEvent memory)
    {
        require(eventId < custodyEvents[evidenceId].length, "invalid eventId");
        return custodyEvents[evidenceId][eventId];
    }
}

