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
                    labels: {
                        fontColor: 'black'
                    }
                }
            },
            scales: {
                x: {
                    stacked: false // Bary vedle sebe
                },
                y: {
                    stacked: false // Bary vedle sebe
                }
            }
        }
    });
});