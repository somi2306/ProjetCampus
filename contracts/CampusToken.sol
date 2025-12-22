// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title CampusToken - Monnaie interne du campus
/// @notice Token ERC20 standard avec une offre initiale fixe
contract CampusToken {
    // Métadonnées du Token
    string public name = "Campus Coin";
    string public symbol = "CAMP";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    // Stockage des soldes (Adresse => Montant)
    mapping(address => uint256) public balanceOf;
    // Stockage des autorisations (Propriétaire => Dépensier => Montant)
    mapping(address => mapping(address => uint256)) public allowance;

    // Événements pour la traçabilité sur la Blockchain
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    /// @notice Initialise le token et attribue tout au déployeur
    /// @param _initialSupply Le montant total de tokens (sans les décimales)
    constructor(uint256 _initialSupply) {
        // Création de la masse monétaire initiale vers le créateur du contrat (Admin)
        _mint(msg.sender, _initialSupply * 10 ** uint256(decimals));
    }

    /// @dev Fonction interne pour la création de tokens
    function _mint(address to, uint256 amount) internal {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    /// @notice Transférer des tokens vers un destinataire
    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Solde insuffisant");
        
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    /// @notice Autoriser une tierce partie (ex: Contrat de Paiement) à dépenser mes tokens
    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    /// @notice Transfert délégué (utilisé par le contrat de paiement)
    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        require(balanceOf[from] >= amount, "Solde insuffisant");
        require(allowance[from][msg.sender] >= amount, "Allowance insuffisante");

        balanceOf[from] -= amount;
        allowance[from][msg.sender] -= amount;
        balanceOf[to] += amount;

        emit Transfer(from, to, amount);
        return true;
    }
}