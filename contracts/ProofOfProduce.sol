pragma solidity ^0.4.24;

// this smart contract is based on the original work of:
// https://www.microsoft.com/developerblog/2018/02/26/using-private-ethereum-consortium-network-store-validate-documents/
//
contract ProofOfProduce {
    struct Proof {
        address owner;
        string encryptedProof;
        string publicProof;
        string previousTrackingId;
    }

    mapping (string => Proof) private proofs;

    mapping (string => mapping (address => bool)) private isTransferred;

    event StoreProofCompleted(
        address from,
        string trackingId,
        string previousTrackingId
    );

    event TransferCompleted(
        address from,
        address to,
        string trackingId
    );

    constructor () public {
    }

    function storeProof(string trackingId,
        string previousTrackingId,
        string encryptedProof,
        string publicProof) public returns (bool success) {

        if (hasProof(trackingId)) {
            return false;
        }

        if (keccak256(abi.encodePacked(previousTrackingId)) != keccak256(abi.encodePacked("root"))) {
            Proof memory p = getProofInternal(previousTrackingId);
            if (msg.sender != p.owner && !isTransferred[previousTrackingId][msg.sender]) {
                return false;
            }
        }

        proofs[trackingId] = Proof(msg.sender, encryptedProof, publicProof, previousTrackingId);
        emit StoreProofCompleted(msg.sender, trackingId, previousTrackingId);

        return true;
    }

    function transfer(string trackingId,
        address newOwner) public returns (bool success) {

        if (hasProof(trackingId)) {
            Proof memory p = getProofInternal(trackingId);
            if (msg.sender == p.owner) {
                isTransferred[trackingId][newOwner] = true;
                emit TransferCompleted(msg.sender, newOwner, trackingId);
            }

            return true;
        }

        return false;
    }

    function hasProof(string trackingId) constant internal returns (bool exists) {

        return proofs[trackingId].owner != address(0);
    }

    function getProofInternal(string trackingId) constant internal returns (Proof proof) {

        if (hasProof(trackingId)) {
            return proofs[trackingId];
        }

        revert();
    }

    function getProof(string trackingId) constant public returns (address owner, string encryptedProof, string publicProof, string previousTrackingId) {

        if (hasProof(trackingId)) {
            Proof memory p = getProofInternal(trackingId);
            owner = p.owner;
            encryptedProof = p.encryptedProof;
            publicProof = p.publicProof;
            previousTrackingId = p.previousTrackingId;
        }
    }

    function getEncryptedProof(string trackingId) constant public returns (string encryptedProof) {

        if (hasProof(trackingId)) {
            return getProofInternal(trackingId).encryptedProof;
        }
    }

    function getPublicProof(string trackingId) constant public returns (string publicProof) {
        
        if (hasProof(trackingId)) {
            return getProofInternal(trackingId).publicProof;
        }
    }

    function getOwner(string trackingId) constant public returns (address owner) {
        if (hasProof(trackingId)) {
            return getProofInternal(trackingId).owner;
        }
    }

    function getPreviousTrackingId (string trackingId) constant public returns (string previousTrackingId) {
        if (hasProof(trackingId)) {
            return getProofInternal(trackingId).previousTrackingId;
        }
    }
}

