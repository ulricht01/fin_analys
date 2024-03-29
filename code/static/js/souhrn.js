fetch('/zustatky_line_chart').then(response => response.json()).then(data => {
    const datumy = data.datumy;
    const zustatky = data.zustatky;

    const ctx = document.getElementById('souhrn_line_chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: datumy,
            datasets: [{
                label: 'Zůstatek',
                data: zustatky,
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
                    text: 'Vývoj zůstatku',
                    font: {
                        size: 18
                    }
                }
            },
            scales: {
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)' // Zde můžete změnit barvu mřížek na osách y
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)' // Zde můžete změnit barvu mřížek na osách x
                    }
                }
            }
        }

    })
})

fetch('/zustatky_bar').then(response => response.json()).then(data => {
    const datumy = data.datumy;
    const prijem = data.prijem;
    const vydej = data.vydej;

    const ctx = document.getElementById('souhrn_bar_chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: datumy,
            datasets: [{
                label: 'Příjem',
                data: prijem,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Výdaj',
                data: vydej,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'x', // Horizontální sloupcový graf
            plugins: {
                title: {
                    display: true,
                    text: 'Vývoj příjmů a výdajů',
                    font: {
                        size: 18
                    }
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        fontColor: 'black'
                    }
                }
            },
            scales: {
                x: {
                    stacked: false, // Bary vedle sebe
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)' // Zde můžete změnit barvu mřížek na osách y
                    }
                },
                y: {
                    stacked: false, // Bary vedle sebe
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)' // Zde můžete změnit barvu mřížek na osách y
                    }
                }
            }
        }
    });
});

fetch('/zustatky_bar_monthly').then(response => response.json()).then(data => {
    const datumy = data.datumy;
    const prijem = data.prijem;
    const vydej = data.vydej;

    const ctx = document.getElementById('souhrn_bar_monthly').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: datumy,
            datasets: [{
                label: 'Příjem',
                data: prijem,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Výdaj',
                data: vydej,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'x', // Horizontální sloupcový graf
            plugins: {
                title: {
                    display: true,
                    text: 'Vývoj příjmů a výdajů',
                    font: {
                        size: 18
                    }
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        fontColor: 'black'
                    }
                }
            },
            scales: {
                x: {
                    stacked: false, // Bary vedle sebe
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)' // Zde můžete změnit barvu mřížek na osách y
                    }
                },
                y: {
                    stacked: false, // Bary vedle sebe
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)' // Zde můžete změnit barvu mřížek na osách y
                    }
                }
            }
        }
    });
});

fetch('/souhrn_pie').then(response => response.json()).then(data => {
    const labels = data.labels;
    const czk = data.czk;

    // Vytvoření grafu pomocí Chart.js
    const ctx = document.getElementById('souhrn_pie_chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Kč',
                data: czk,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 99, 132, 0.5)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
            },
            plugins:{
            legend:{
                display: true,
                position: 'bottom'
            },
            title: {
                display: true,
                text: 'Příjmy vs Výdaje',
                font: {
                    size: 18
                }
            }
        }
    }
    });
}).catch(error => {
    console.error('Chyba při načítání dat:', error);
});