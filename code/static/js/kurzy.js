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
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: true
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
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: true
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
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: true
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