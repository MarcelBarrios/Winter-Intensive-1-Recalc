document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("saved-calculations");
    const ctx = document.getElementById('savingsChart').getContext('2d');
    let savingsChart;

    const updateGraph = (years, balances) => {
        if (savingsChart) {
            savingsChart.destroy(); // Destroy the old chart before creating a new one
        }
        savingsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: years,
                datasets: [{
                    label: 'Projected Savings',
                    data: balances,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: false,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Year'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Savings ($)'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    };

    const updateResults = (profession, totalSavings) => {
        document.getElementById("selected-profession").textContent = profession;
        document.getElementById("total-savings").textContent = totalSavings.toFixed(2);
    };

    container.addEventListener("click", (event) => {
        const target = event.target;

        // Check if the clicked element is a "show graph" button
        if (target.classList.contains("show-graph-button")) {
            const calculationId = target.dataset.id;
            fetch(`/get_graph_data/${calculationId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.years && data.balances) {
                        updateGraph(data.years, data.balances);
                        updateResults(data.profession, data.total_savings_at_retirement);
                    } else {
                        alert("Failed to fetch graph data.");
                    }
                })
                .catch(error => {
                    console.error("Error fetching graph data:", error);
                    alert("An error occurred while fetching graph data.");
                });
        }
    });
});
