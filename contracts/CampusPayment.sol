// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Interface minimale pour interagir avec le Token ERC20
interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

/// @title CampusPayment - Gestion des paiements étudiants
/// @notice Permet de régler des services (Cantine, Pressing) en tokens CAMP
contract CampusPayment {
    IERC20 public token;
    address public owner;

    // Structure définissant un service du campus
    struct Service {
        string name;
        address wallet; // Adresse qui reçoit les fonds
        uint256 price;  // Prix de référence en tokens
    }

    // Liste dynamique des services disponibles
    Service[] public services;

    // Événement émis à chaque achat pour l'historique (Frontend Explorer)
    event PaymentMade(address indexed student, string service, uint256 amount, uint256 timestamp);

    /// @notice Déploiement du contrat
    /// @param _tokenAddress L'adresse du contrat CampusToken précédemment déployé
    constructor(address _tokenAddress) {
        token = IERC20(_tokenAddress);
        owner = msg.sender;

        // Les adresses GANACHE (À configurer)
        services.push(Service("Cantine", 0x2EB6663cF256B5Da2e6479241653dc1c138A3c80, 10));
        services.push(Service("Pressing", 0x024fF415536E28F0B2861586Ee7C4b83B13909FC, 5));
    }

    function getServicesCount() public view returns (uint) {
        return services.length;
    }

    /// @notice Effectue le paiement d'un service
    /// @dev Nécessite une approbation (approve) préalable sur le contrat Token
    /// @param _serviceId L'index du service dans le tableau
    /// @param _amount Le montant à payer
    function payService(uint _serviceId, uint256 _amount) public {
        require(_serviceId < services.length, "Service inconnu");
        
        Service memory srv = services[_serviceId];

        // Exécution du transfert : Étudiant -> Service
        // On multiplie par 10^18 pour gérer les décimales du token
        bool success = token.transferFrom(msg.sender, srv.wallet, _amount * 10**18);
        require(success, "Paiement echoue (Verifiez l'approve)");

        // Enregistrement de la transaction sur la Blockchain
        emit PaymentMade(msg.sender, srv.name, _amount, block.timestamp);
    }
}