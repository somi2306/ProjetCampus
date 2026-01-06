// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title CampusToken - Monnaie interne du campus
/// @notice Token ERC20 standard avec une offre initiale fixe
contract CampusToken {
    // Métadonnées du Token
    string public name = "Campus Coin";
    string public symbol = "CAMP";
    uint8 public decimals = 18; // Nombre de décimales pour le token comme le blockchain ne gère pas les nombres à virgule (ex: $1.5$), on stocke tout en entiers très grands (en Wei)
    //LE standard absolu d'Ethereum est 18 décimales
    uint256 public totalSupply; // Total des tokens en circulation pour toutes les comptes càd la somme de toutes les montants = totalSupply et il est public pour qu'on puisse le lire de l'extérieur
//on limite pour Confiance et de Valeur
    // Stockage des soldes (Adresse => Montant)
    mapping(address => uint256) public balanceOf; // Solde de chaque compte
    // Stockage des autorisations (Propriétaire => Dépensier => Montant)
    mapping(address => mapping(address => uint256)) public allowance; // Autorisation donnée par le propriétaire à un dépensier(ContratPaiement) de dépenser une certaine quantité de tokens en son nom

    //les var balanceOf ne ne stockent que l'état ACTUEL des soldes, mais les événements permettent de reconstruire l'historique des transactions
    event Transfer(address indexed from, address indexed to, uint256 value);
    // l'argument 'indexed' permet de filtrer les événements par ces paramètres
    event Approval(address indexed owner, address indexed spender, uint256 value);
    // l'authorisation est un événement important pour les contrats de paiement délégué

    /// @notice Initialise le token et attribue tout au déployeur
    /// @param _initialSupply Le montant total de tokens (sans les décimales)
    constructor(uint256 _initialSupply) {
        // Création de la masse monétaire initiale vers le créateur du contrat (Admin)
        _mint(msg.sender, _initialSupply * 10 ** uint256(decimals));
    }

    /// @dev Fonction interne pour la création de tokens
    //_mint (Création) : On augmente totalSupply car on injecte de la nouvelle monnaie dans l'économie
    function _mint(address to, uint256 amount) internal {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);//l’adresse nulle
    }

    /// @notice Transférer des tokens vers un destinataire
    //Dans transfer (Circulation) : il n'y a PAS de totalSupply += amount car on ne crée pas de nouvelle monnaie, on la fait juste circuler entre les comptes
    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Solde insuffisant");
        //change selon QUI appelle la fonction
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    /// @notice Autoriser une tierce partie (ex: Contrat de Paiement) à dépenser mes tokens
    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;//Définit la limite maximale autorisée
        emit Approval(msg.sender, spender, amount);//Trace l’autorisation sur la blockchain
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