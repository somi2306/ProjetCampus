import pytest
from web3 import Web3
from web3.exceptions import ContractLogicError # <--- L'import manquant
import json

# Configuration
GANACHE_URL = "http://127.0.0.1:7545"

@pytest.fixture
def setup():
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    
    # On charge la config
    with open("frontend/conf.json", "r") as f:
        conf = json.load(f)
    
    payment = w3.eth.contract(address=conf["paymentAddress"], abi=conf["paymentABI"])
    token = w3.eth.contract(address=conf["tokenAddress"], abi=conf["tokenABI"])
    
    # On prend un étudiant "pauvre" (compte n°9) qui n'a rien reçu
    student = w3.eth.accounts[9]
    return w3, payment, token, student

def test_cannot_pay_without_funds(setup):
    """Vérifie qu'un étudiant sans argent ne peut pas payer"""
    w3, payment, token, student = setup
    
    print("\nTest Sécurité 1 : Tentative de paiement sans fonds...")
    
    # L'étudiant essaie de payer sans avoir de tokens
    try:
        payment.functions.payService(0, 10).transact({'from': student})
        # Si la ligne ci-dessus ne plante pas, c'est que le test a échoué
        pytest.fail("FAIL : Le contrat aurait dû rejeter la transaction !")
    except (ContractLogicError, ValueError) as e:
        # On vérifie que le message d'erreur contient bien la raison du rejet
        error_msg = str(e)
        print(f"   (Erreur reçue : {error_msg})")
        assert "Solde insuffisant" in error_msg or "revert" in error_msg
        print("SUCCÈS : Transaction rejetée comme prévu (Pas d'argent)")

def test_cannot_pay_without_approval(setup):
    """Vérifie qu'on ne peut pas payer sans 'approve' (Vol de tokens impossible)"""
    w3, payment, token, student = setup
    admin = w3.eth.accounts[0]
    
    # On donne de l'argent à l'étudiant (50 CAMP)
    token.functions.transfer(student, w3.to_wei(50, 'ether')).transact({'from': admin})
    
    print("\nTest Sécurité 2 : Tentative de paiement sans approbation...")
    
    # Il a l'argent, MAIS il n'a pas fait 'approve' au contrat de paiement
    try:
        payment.functions.payService(0, 10).transact({'from': student})
        pytest.fail("FAIL : Le contrat aurait dû rejeter sans approve !")
    except (ContractLogicError, ValueError) as e:
        error_msg = str(e)
        print(f"   (Erreur reçue : {error_msg})")
        assert "Allowance insuffisante" in error_msg or "revert" in error_msg
        print("SUCCÈS : Transaction rejetée comme prévu (Pas d'approbation)")