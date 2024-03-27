
// Načtení dat z databáze pomocí AJAX
fetch('/vydaje_pie').then(response => response.json()).then(data => {
    const labels = data.labels;
    const values = data.data;

    // Vytvoření grafu pomocí Chart.js
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: '',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                    'rgba(200, 100, 35, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(200, 100, 35, 1)'
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
                position: 'left'
            },
            title: {
                display: true,
                text: 'Dle kategorií',
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

fetch('/vydaje_bar').then(response => response.json()).then(data => {
    const labels = data.labels;
    const values = data.data;

    const ctx = document.getElementById('myChart2').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',

                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Dle dní',
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

fetch('/vydaje_month_bar').then(response => response.json()).then(data => {
    const labels = data.labels;
    const values = data.data;

    const ctx = document.getElementById('myChart3').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',

                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Dle měsíců',
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