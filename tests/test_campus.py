import pytest
from web3 import Web3

# Configuration
GANACHE_URL = "http://127.0.0.1:7545"

@pytest.fixture
def w3():
    #Fixture Pytest qui initialise la connexion Web3 avant chaque test
    w3_instance = Web3(Web3.HTTPProvider(GANACHE_URL))
    return w3_instance

def test_connection(w3):
    #Vérification que le script peut bien parler au noeud blockchain local
    assert w3.is_connected() == True, "Échec de connexion à Ganache et vérifiez le port"

def test_accounts_exist(w3):
    #Vérification que Ganache a bien généré les 10 comptes de test par défaut
    accounts = w3.eth.accounts
    assert len(accounts) > 0, "Aucun compte détecté"

def test_admin_balance(w3):
    #Le premier compte (Admin) doit avoir de l'ETH pour payer le gaz du déploiement
    admin = w3.eth.accounts[0]
    balance_wei = w3.eth.get_balance(admin)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    
    assert balance_eth > 0, "Le compte Admin n'a pas d'ETH pour le Gaz"