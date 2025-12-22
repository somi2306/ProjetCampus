# 🎓 Projet Campus (Blockchain DApp)

**ProjetCampus** est une application décentralisée (DApp) conçue pour la gestion économique d'un campus étudiant via la Blockchain. Elle permet l'émission d'une monnaie interne (CampusToken) et la gestion des paiements sécurisés entre l'administration, les étudiants et les services du campus.

---

## 🏗 Architecture & Stack Technique

Le projet repose sur une architecture Web3 standard :

### 🔗 Smart Contracts (`contracts/`)
* **Langage** : Solidity
* **CampusToken.sol** : Token ERC-20 standard représentant la monnaie du campus.
* **CampusPayment.sol** : Contrat de gestion des transactions, des paiements et des interactions financières.

### 💻 Frontend (`frontend/`)
* **Interface** : HTML5 / Tailwind / JavaScript
* **Web3 Integration** : Utilisation de `Web3.js`  pour interagir avec la blockchain.
* **Rôles** :
    * `admin.html` : Interface d'administration pour la gestion des tokens.
    * `student.html` : Interface pour les étudiants (solde, paiements).
    * `explorer.html` : Explorateur de transactions ou de données publiques.

### ⚙️ Déploiement & Tests (`scripts/`, `tests/`)
* **Scripts** : `deploy.py` pour le déploiement sur le réseau.
* **Tests** : `test_campus.py` pour valider la logique des contrats.

---

## 🚀 Installation et Configuration

### Prérequis
* **Python** (v3.8+)
* **Ganache** (pour la blockchain locale)
* **Metamask** (Extension navigateur pour interagir avec le frontend)

### 1. Installation des dépendances

> [!IMPORTANT]
> Il est recommandé d'utiliser un environnement virtuel Python.

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances Python
pip install -r requirements.txt
```

### 2. Configuration avant déploiement

Avant de lancer le script, assurez-vous de configurer les services et le compte administrateur avec vos données Ganache.

**1. Dans `contracts/CampusPayment.sol`** (Pour définir les services initiaux) :
```solidity
services.push(Service("Cantine", 0x2EB6...3c80, 10));
services.push(Service("Pressing", 0x024f...09FC, 5));
```

**2. Dans `scripts/deploy.py`** (Pour définir l'Admin qui déploie (le premier compte de Ganache)) :
```python
# Clé publique
my_address = "0x39A5...d6aF"
# Clé privée
private_key = "0x340a...7c1a"
```

**3. Dans `frontend/admin.js`** (Pour les paiements) :
```Javascript
const ADDR_CANTINE = "0x2EB6...3c8"; 
const ADDR_PRESSING = "0x024f...09FC";
```

### 3. Déploiement

Vous avez deux options pour déployer l'environnement et les contrats :

#### Option 1 : Via Docker (Recommandé)
Le fichier `docker-compose.yml` permet de lancer l'environnement complet.

```bash
docker-compose up --build
```

#### Option 2 : Déploiement Manuel (Local)
1. **Lancer la Blockchain** : Démarrez Ganache pour avoir une blockchain locale active.
2. **Déployer les contrats** : Utilisez le script Python dédié.

```bash
# Via script Python standard
python scripts/deploy.py
```

> [!NOTE]
> **Important :** Une fois le déploiement terminé, notez bien l'adresse des contrats déployés (`CampusToken` et `CampusPayment`) pour ajuter ce token en metamask.

## 🖥️ Utilisation du Frontend

L'application ne nécessite pas de serveur complexe, il s'agit de fichiers statiques interagissant avec la blockchain.

### Lancer le serveur local

```bash
cd frontend/
python -m http.server 8000
```

### Accéder aux interfaces

Ouvrez votre navigateur et accédez aux pages suivantes :

| Interface | URL | Description |
| :--- | :--- | :--- |
| **Admin** | `http://localhost:8000/admin.html` | Mint de tokens, gestion des droits et configuration. |
| **Étudiant** | `http://localhost:8000/student.html` | Visualisation du solde, effectuer un paiement. |
| **Explorer** | `http://localhost:8000/explorer.html` | Vue d'ensemble des activités et transactions publiques. |

> [!TIP]
> **Configuration Metamask :** Assurez-vous que votre extension Metamask est connectée au réseau local  de Ganache (`Localhost 7545`) et que vous avez importé les clés privées (comptes de test) fournies par Ganache pour simuler les transactions.

## 🧪 Tests

Pour valider la logique des Smart Contracts, exécutez la suite de tests unitaires et d'intégration :

```bash
# Via Pytest
pytest tests/test_campus.py
```
