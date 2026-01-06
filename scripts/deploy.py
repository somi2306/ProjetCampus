import json
from web3 import Web3 # Connexion à la blockchain locale
from solcx import compile_standard, install_solc # Compilation des contrats Solidity

# 1. Configuration de l'environnement
install_solc("0.8.0") # Installation automatique du compilateur Solidity

# Connexion au nœud local Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337 # ID de la chaîne Ganache par défaut

# Adresse de l'administrateur (le premier compte de Ganache : À configurer)
my_address = "0x39A5fe52856fdefa05c23F23b84D5901038bd6aF" 
private_key = "0x340a49376705f23ea938945b9dd4bc0d20ec8495d801b54de746ff9fb5287c1a" # Clé privée de l'admin : signer les transactions

def compile_and_deploy():
    #Compilation des contrats Solidity et les déploie sur la blockchain locale
    
    print("Démarrage du déploiement")

    # 2. Lecture et Compilation des sources
    print("1. Compilation des contrats")
    
    with open("./contracts/CampusToken.sol", "r") as f: token_src = f.read()
    with open("./contracts/CampusPayment.sol", "r") as f: pay_src = f.read()
    #solc compile le code Solidity
    compiled = compile_standard({
        "language": "Solidity",
        "sources": {
            "CampusToken.sol": {"content": token_src},
            "CampusPayment.sol": {"content": pay_src}
        },
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}} # api pour le binaire 
    }, solc_version="0.8.0")
    #Le Bytecode (evm.bytecode) : C'est le code binaire (Programme) qui sera stocké sur la Blockchain dans l'adresse de smart contract. 
    # Il contient : La logique des fonctions, La logique des variables, Les instructions EVM 
    #Le bytecode NE contient PAS : Les valeurs des variables (balances, totalSupply…), Les données des events, Les arguments des fonctions
    #L'ABI (abi) : C'est le "mode d'emploi" (Application Binary Interface). C'est un fichier JSON qui liste les fonctions disponibles (transfer, approve...). Sans ABI, le site web ne sait pas comment parler au contrat.
    #L’ABI sert à encoder ET décoder les données entre le frontend et l’EVM, mais l’EVM lui-même ne “lit” pas l’ABI
    # 3. Déploiement du Token (ERC20)
    print("2. Déploiement du CampusToken")
    
    # Récupération du Bytecode et de l'ABI (Interface)
    bytecode_token = compiled["contracts"]["CampusToken.sol"]["CampusToken"]["evm"]["bytecode"]["object"]
    abi_token = compiled["contracts"]["CampusToken.sol"]["CampusToken"]["abi"]

    TokenContract = w3.eth.contract(abi=abi_token, bytecode=bytecode_token)
    nonce = w3.eth.get_transaction_count(my_address)

    # Création de la transaction de déploiement avec initialisation de 1 000 000 jetons
    tx = TokenContract.constructor(1000000).build_transaction({
        "chainId": chain_id, 
        "from": my_address, 
        "nonce": nonce
    })
    
    # Signature et envoi
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key) #Python utilise votre Clé Privée pour sceller cryptographiquement la transaction.
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)#On attend que Ganache mine le bloc
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)#Ganache répond "C'est bon, c'est gravé ! Voici la nouvelle adresse du contrat".
    
    token_address = tx_receipt.contractAddress #Adresse du contrat Token déployé
    print(f"   > Token déployé à l'adresse : {token_address}")

    # 4. Déploiement du Système de Paiement
    print("3. Déploiement du CampusPayment")
    
    bytecode_pay = compiled["contracts"]["CampusPayment.sol"]["CampusPayment"]["evm"]["bytecode"]["object"]
    abi_pay = compiled["contracts"]["CampusPayment.sol"]["CampusPayment"]["abi"]

    PayContract = w3.eth.contract(abi=abi_pay, bytecode=bytecode_pay)
    nonce = w3.eth.get_transaction_count(my_address)

    # On passe l'adresse du Token au constructeur du contrat de paiement
    tx = PayContract.constructor(token_address).build_transaction({
        "chainId": chain_id, 
        "from": my_address, 
        "nonce": nonce
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    pay_address = tx_receipt.contractAddress
    print(f"   > Système de Paiement déployé à l'adresse : {pay_address}")

    # 5. Export de la configuration pour le Frontend pour permettre au site web de connaître automatiquement les nouvelles adresses
    config = {
        "tokenAddress": token_address,
        "tokenABI": abi_token,
        "paymentAddress": pay_address,
        "paymentABI": abi_pay
    }
    
    with open("./frontend/conf.json", "w") as f:
        json.dump(config, f)
    print("4. Configuration frontend sauvegardée dans frontend/conf.json")
    print("Déploiement terminé avec succès")

if __name__ == "__main__":
    compile_and_deploy()