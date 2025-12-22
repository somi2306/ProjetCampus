let web3, conf, paymentContract;

async function init() {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        try {
            await window.ethereum.request({ method: 'eth_requestAccounts' });
        } catch (e) {
            console.warn("Lecture sans connexion compte...");
        }
    } else {
        web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));
    }

    const resp = await fetch('conf.json');
    conf = await resp.json();

    paymentContract = new web3.eth.Contract(conf.paymentABI, conf.paymentAddress);

    loadEvents();
}

async function loadEvents() {
    const tableBody = document.getElementById('eventsTable');
    tableBody.innerHTML = '<tr><td colspan="5" class="p-6 text-center text-gray-400">Recherche des blocs...</td></tr>';

    try {
        const events = await paymentContract.getPastEvents('PaymentMade', {
            fromBlock: 0,
            toBlock: 'latest'
        });

        events.reverse();
        tableBody.innerHTML = '';

        if (events.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" class="p-6 text-center text-gray-500">Aucun paiement trouvé sur la blockchain.</td></tr>';
            return;
        }

        for (let event of events) {
            const data = event.returnValues;
            const dateObj = new Date(Number(data.timestamp) * 1000);
            const dateStr = dateObj.toLocaleDateString() + ' ' + dateObj.toLocaleTimeString();
            const amountEth = web3.utils.fromWei(data.amount, 'ether');

            let serviceBadge = `<span class="px-2 py-1 rounded text-xs font-bold bg-gray-200 text-gray-700">${data.service}</span>`;
            if(data.service === "Cantine") serviceBadge = `<span class="px-2 py-1 rounded text-xs font-bold bg-green-100 text-green-800">🍔 Cantine</span>`;
            if(data.service === "Pressing") serviceBadge = `<span class="px-2 py-1 rounded text-xs font-bold bg-purple-100 text-purple-800">👔 Pressing</span>`;

            const row = `
                <tr class="hover:bg-blue-50 transition border-b border-gray-100">
                    <td class="p-4 text-gray-600">${dateStr}</td>
                    <td class="p-4 font-mono text-blue-600 text-xs break-all">${data.student}</td>
                    <td class="p-4">${serviceBadge}</td>
                    <td class="p-4 text-right font-bold text-gray-800">${amountEth} CAMP</td>
                    <td class="p-4 text-center text-gray-400 text-xs">#${event.blockNumber}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        }

    } catch (error) {
        console.error(error);
        tableBody.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-red-500">Erreur de lecture : ${error.message} (Vérifiez Ganache)</td></tr>`;
    }
}

// Événements
document.getElementById('refreshEventsBtn')?.addEventListener('click', loadEvents);
window.addEventListener('load', init);