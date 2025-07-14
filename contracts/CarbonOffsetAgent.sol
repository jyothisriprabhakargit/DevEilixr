// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CarbonOffsetAgent {
    address public admin;

    // Mapping to store emissions and credits per user
    mapping(address => uint256) public emissions;
    mapping(address => uint256) public carbonCredits;

    // Events for logging
    event EmissionLogged(address indexed user, uint256 amount);
    event OffsetPerformed(address indexed user, uint256 amount);
    event CreditsAdded(address indexed user, uint256 amount);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this.");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    // Admin logs emissions for a user
    function logEmissions(address user, uint256 amount) external onlyAdmin {
        emissions[user] += amount;
        emit EmissionLogged(user, amount);
    }

    // Admin offsets emissions using credits
    function offset(address user) external onlyAdmin {
        uint256 emission = emissions[user];
        require(carbonCredits[user] >= emission, "Not enough credits");
        carbonCredits[user] -= emission;
        emissions[user] = 0;
        emit OffsetPerformed(user, emission);
    }

    // Admin adds credits to a user
    function addCredits(address user, uint256 amount) external onlyAdmin {
        carbonCredits[user] += amount;
        emit CreditsAdded(user, amount);
    }

    // Public view function to check status
    function getStatus(address user) external view returns (uint256, uint256) {
        return (emissions[user], carbonCredits[user]);
    }
    // Payment-based offset function
function payToOffset() external payable {
    require(emissions[msg.sender] > 0, "No emissions to offset");
    require(msg.value > 0, "Payment required to offset");

    uint256 amount = emissions[msg.sender];
    emissions[msg.sender] = 0;

    emit OffsetPerformed(msg.sender, amount);
}

}
