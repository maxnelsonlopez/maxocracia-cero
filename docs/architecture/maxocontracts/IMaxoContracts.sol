// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IMaxoContracts
 * @dev Interface for the Maxocracia Ethical Smart Contracts (Capa 4 - Legal)
 * 
 * Based on the 8 Axioms of Truth and the 15 Temporal Axioms.
 */
interface IMaxoContracts {
    
    enum ContractState { DRAFT, PENDING, ACTIVE, EXECUTED, PARTIAL, RETRACTED }
    
    struct VHV {
        uint256 T; // Time in seconds (TVI)
        uint256 V; // Life impact (Units of Life Consumed)
        uint256 R; // Resource usage
    }
    
    struct Term {
        bytes32 termId;
        string description; // Civil language, max 20 words
        VHV cost;
        bool isCooperative;
    }

    /**
     * @dev Validates a contract against axiomatic invariants.
     * Axiom T7: Minimize harm (V cannot increase without justification)
     * Invariant 1: Wellness >= 1.0
     * Invariant 2: SDV (Suelo de Dignidad Vital) respected
     */
    function validateAxioms(bytes32 contractId) external view returns (bool, string[] memory violations);

    /**
     * @dev Registers a new term-by-term acceptance.
     * Implements "Aceptación Término-a-Término" (Axiom T13).
     */
    function acceptTerm(bytes32 contractId, bytes32 termId) external;

    /**
     * @dev Triggers an ethical retraction.
     * Invariant 4: Guaranteed Retractability.
     */
    function triggerRetraction(bytes32 contractId, string calldata reason) external;

    /**
     * @dev Returns the current Wellness Index of a participant.
     * Wellness < 1.0 (Gamma) triggers safety protocols.
     */
    function getWellnessIndex(address participant) external view returns (uint256);
}

/**
 * @title IMaxoOracle
 * @dev Interface for Dynamic Oracles (Human + Synthetic)
 */
interface IMaxoOracle {
    /**
     * @dev Provides technical validation for a VHV calculation.
     */
    function verifyVHV(bytes32 calculationId, VHV calldata values) external returns (bool);
    
    /**
     * @dev Updates global valuation parameters (Alpha, Beta, Gamma, Delta).
     * Must be called via consensus (Axiom 7).
     */
    function updateParameters(uint256 alpha, uint256 beta, uint256 gamma, uint256 delta) external;
}
