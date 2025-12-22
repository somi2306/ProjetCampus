let web3, conf, tokenContract;
let accounts;

// Les adresses GANACHE (À configurer)
const ADDR_CANTINE = "0x2EB6663cF256B5Da2e6479241653dc1c138A3c80"; 
const ADDR_PRESSING = "0x024fF415536E28F0B2861586Ee7C4b83B13909FC"; 

async function init() {
    const resp = await fetch('conf.json');
    conf = await resp.json();
}

async function connectWallet() {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        accounts = await web3.eth.getAccounts();
        
        await init();
        tokenContract = new web3.eth.Contract(conf.tokenABI, conf.tokenAddress);

        document.getElementById('accountDisplay').innerText = "Connecté : " + accounts[0];
        document.getElementById('connectBtn').style.display = 'none';

        document.getElementById('addrCantine').innerText = ADDR_CANTINE;
        document.getElementById('addrPressing').innerText = ADDR_PRESSING;

        updateBalances();
    } else {
        alert("Installez MetaMask");
    }
}

async function updateBalances() {
    try {
        // 1. Solde Cantine
        const b1 = await tokenContract.methods.balanceOf(ADDR_CANTINE).call();
        document.getElementById('balCantine').innerText = web3.utils.fromWei(b1, 'ether');

        // 2. Solde Pressing
        const b2 = await tokenContract.methods.balanceOf(ADDR_PRESSING).call();
        document.getElementById('balPressing').innerText = web3.utils.fromWei(b2, 'ether');

        // 3. Solde de l'Admin connecté
        if (accounts && accounts[0]) {
            const adminBal = await tokenContract.methods.balanceOf(accounts[0]).call();
            document.getElementById('adminBalanceDisplay').innerText = web3.utils.fromWei(adminBal, 'ether');
        }

    } catch (e) {
        console.error(e);
    }
}

async function sendTokens() {
    const toAddr = document.getElementById('faucetAddress').value;
    const amount = document.getElementById('faucetAmount').value;

    if(!web3.utils.isAddress(toAddr)) {
        alert("Adresse invalide");
        return;
    }

    try {
        const amountWei = web3.utils.toWei(amount.toString(), 'ether');
        console.log(`Envoi de ${amount} CAMP vers ${toAddr}...`);
        
        await tokenContract.methods.transfer(toAddr, amountWei)
            .send({ from: accounts[0] }); 

        alert("Tokens envoyés avec succès");
        updateBalances(); 
    } catch (error) {
        console.error(error);
        alert("Erreur : Vérifiez que vous êtes connecté avec le Compte Admin");
    }
}

// Événements
document.getElementById('connectBtn').addEventListener('click', connectWallet);
document.getElementById('refreshBtn').addEventListener('click', updateBalances);
document.getElementById('sendTokensBtn').addEventListener('click', sendTokens);