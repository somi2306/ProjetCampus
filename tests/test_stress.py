import time
import json
import random
from web3 import Web3
from concurrent.futures import ThreadPoolExecutor

# 1. Connexion au "Moteur" (Ganache)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.is_connected():
    print("Erreur : Impossible de se connecter à Ganache via le port 7545")
    exit()

# 2. Chargement de la Configuration (Générée par deploy.py)
try:
    with open("frontend/conf.json", "r") as f:
        conf = json.load(f)
except FileNotFoundError:
    print("Erreur : Fichier frontend/conf.json introuvable. Lancez 'python scripts/deploy.py' d'abord.")
    exit()

# 3. Initialisation des Contrats
payment_contract = w3.eth.contract(address=conf["paymentAddress"], abi=conf["paymentABI"])
token_contract = w3.eth.contract(address=conf["tokenAddress"], abi=conf["tokenABI"])

# 4. Préparation des Acteurs
admin = w3.eth.accounts[0]  # Celui qui paie
print("--- DÉMARRAGE DU STRESS TEST ---")
print(f"Compte payeur : {admin}")

# --- Étape d'Approbation ---
print("1. Approbation du contrat de paiement...")
tx_approve = token_contract.functions.approve(
    conf["paymentAddress"], 
    w3.to_wei(1000000, 'ether')  # Montant élevé pour éviter les soucis
).transact({'from': admin})
w3.eth.wait_for_transaction_receipt(tx_approve)
print("Approbation validée sur la Blockchain.")

# 5. Boucle de Paiement (Parallélisée)
def send_payment(i):
    try:
        # On choisit aléatoirement : 0 (Cantine) ou 1 (Pressing)
        service_id = random.choice([0, 1])
        
        # LOGIQUE INTELLIGENTE : On adapte le prix
        amount = 0
        if service_id == 0:
            amount = 10 # Prix Cantine
        else:
            amount = 5  # Prix Pressing
        
        tx_hash = payment_contract.functions.payService(
            service_id, 
            amount # On envoie le VRAI prix
        ).transact({'from': admin})
        
        return f"Tx #{i} envoyée pour le service {service_id} ({amount} CAMP)"
    except Exception as e:
        return f" Erreur #{i} : {e}"

print("2. Lancement de 50 transactions en parallèle...")
start_time = time.time()

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(send_payment, range(50)))

end_time = time.time()
duration = end_time - start_time

# 6. Bilan de performance
success_count = sum(1 for r in results if "Transaction" in r)
print("\n--- RÉSULTAT DU BENCHMARK ---")
print(f"Transactions soumises : {success_count}/50")
print(f"Temps écoulé : {duration:.2f} secondes")
print(f"Débit (TPS) : {50/duration:.2f} transactions/seconde")