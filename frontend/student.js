let web3;
let accounts;
let tokenContract; //instance du smart contract CampusToken
let paymentContract; //instance du smart contract CampusPayment
let conf;
async function loadConfig() {
    const response = await fetch('conf.json');
    conf = await response.json();
}

document.getElementById('connectBtn').addEventListener('click', async () => {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        
        try {
            // 1. Demande de connexion (avec gestion d'erreur si on annule)
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            accounts = await web3.eth.getAccounts();
            
            await loadConfig();
            
            // 2. Initialisation des contrats
            tokenContract = new web3.eth.Contract(conf.tokenABI, conf.tokenAddress);
            paymentContract = new web3.eth.Contract(conf.paymentABI, conf.paymentAddress);
            //Grâce à l’ABI, le frontend sait comment appeler les fonctions (transfer, approve, payService
            // 3. Mise à jour de l'interface 
            document.getElementById('connectBtn').style.display = 'none';
            
            const walletInfo = document.getElementById('walletInfo');
            walletInfo.classList.remove('hidden'); 
            walletInfo.style.display = 'block';    
            
            document.getElementById('accountDisplay').innerText = accounts[0];
            
            updateBalance();

        } catch (error) {
            console.error("Erreur connexion:", error);
            alert("Connexion annulée ou erreur réseau."); 
        }
    } else {
        alert("Installez MetaMask");
    }
});

async function updateBalance() {
    try {
        const bal = await tokenContract.methods.balanceOf(accounts[0]).call();
        //call() → lecture seulement, pas de transaction
        // Conversion Wei -> Ether (Token)
        document.getElementById('balanceDisplay').innerText = web3.utils.fromWei(bal, 'ether');
    } catch (error) {
        console.error("Erreur lecture solde:", error);
    }
}

async function approveAndPay(serviceId, amount) {
    if (!tokenContract) {
        alert("Connectez-vous d'abord");
        return;
    }

    const amountWei = web3.utils.toWei(amount.toString(), 'ether');

    try {
        // 1. APPROVE : Autoriser le contrat de paiement à prendre les tokens
        console.log("Approbation en cours...");
        await tokenContract.methods.approve(conf.paymentAddress, amountWei) //Autorise le contrat de paiement à dépenser le montant sur ton compte
            .send({ from: accounts[0] }); //envoie une transaction à la blockchain avec clé privé de meta mask
        console.log("Approuvé !");
        
        // 2. PAY : Exécuter le paiement
        console.log("Paiement en cours...");
        await paymentContract.methods.payService(serviceId, amount)
            .send({ from: accounts[0] });

        alert("Paiement réussi");
        updateBalance();
    } catch (error) {
        console.error(error);
        alert("Erreur lors du paiement");
    }
}

// IMPORTANT : Rendre la fonction accessible aux boutons HTML onclick=""
window.approveAndPay = approveAndPay;