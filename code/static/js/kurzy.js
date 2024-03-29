
function updateRates() {
    fetch('/api/rates')
    .then(response => response.json())
    .then(data => {
        document.getElementById('usd-rate').innerText = data.usd_rate;
        document.getElementById('eur-rate').innerText = data.eur_rate;
        document.getElementById('gbp-rate').innerText = data.gbp_rate;
        document.getElementById('shiba-rate').innerText = data.shiba_rate;
        document.getElementById('bitcoin-rate').innerText = data.bitcoin_rate;
        document.getElementById('doge-rate').innerText = data.doge_rate;
    })
    fetch('/data_line_eur').then(response => response.json()).then(data => {
        const datumy = data.datumy;
        const czk = data.koruny;
    
        const ctx = document.getElementById('kurzy_eur_chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: datumy,
                datasets: [{
                    label: 'EUR',
                    data: czk,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                    title:{
                        display: true,
                        text: 'Vývoj EUR dle dní',
                        font: {
                            size: 18
                        }
                    }
                }
            }
    
        })
    })
    
    fetch('/data_line_usd').then(response => response.json()).then(data => {
        const datumy = data.datumy;
        const czk = data.koruny;
    
        const ctx = document.getElementById('kurzy_usd_chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: datumy,
                datasets: [{
                    label: 'USD',
                    data: czk,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                    title:{
                        display: true,
                        text: 'Vývoj USD dle dní',
                        font: {
                            size: 18
                        }
                    }
                }
            }
    
        })
    })
    
    fetch('/data_line_gbp').then(response => response.json()).then(data => {
        const datumy = data.datumy;
        const czk = data.koruny;
    
        const ctx = document.getElementById('kurzy_gbp_chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: datumy,
                datasets: [{
                    label: 'GBP',
                    data: czk,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                    title:{
                        display: true,
                        text: 'Vývoj GBP dle dní',
                        font: {
                            size: 18
                        }
                    }
                }
            }
    
        })
    })
    
    
    fetch('/krypto_bitcoin_lines').then(response => response.json()).then(data => {
        const casy = data.datumy;
        const hodnoty = data.koruny;
    
        const ctx = document.getElementById('btc_line_chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: casy,
                datasets: [{
                    label: 'CZK',
                    data: hodnoty,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                    title:{
                        display: true,
                        text: 'Průměrný vývoj BITCOIN',
                        font: {
                            size: 18
                        }
                    }
                }
            }
    
        })
    })
    
    fetch('/krypto_shiba_lines').then(response => response.json()).then(data => {
        const casy = data.datumy;
        const hodnoty = data.koruny;
    
        const ctx = document.getElementById('shiba_line_chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: casy,
                datasets: [{
                    label: 'CZK',
                    data: hodnoty,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                    title:{
                        display: true,
                        text: 'Průměrný vývoj SHIBA',
                        font: {
                            size: 18
                        }
                    }
                }
            }
    
        })
    })
    
    fetch('/krypto_doge_lines').then(response => response.json()).then(data => {
        const casy = data.datumy;
        const hodnoty = data.koruny;
    
        const ctx = document.getElementById('doge_line_chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: casy,
                datasets: [{
                    label: 'CZK',
                    data: hodnoty,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                    title:{
                        display: true,
                        text: 'Průměrný vývoj DOGE',
                        font: {
                            size: 18
                        }
                    }
                }
            }
    
        })
    })
    
    
    
    
    ;
}

// Update rates initially
updateRates();

// Update rates every 13 seconds
setInterval(updateRates, 60000);