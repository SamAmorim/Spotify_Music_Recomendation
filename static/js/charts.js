const characteristicsChart = document.getElementById('characteristics-chart');
const musicalityChart = document.getElementById('musicality-chart');
const genresChart = document.getElementById('genres-chart');

Chart.register(ChartDataLabels);

(async function () {
    new Chart(
        characteristicsChart,
        {
            type: 'bar',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: {
                            color: "#fff"
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        ticks: {
                            color: "#fff",
                            callback: value => value + "%"
                        },
                        grid: {
                            color: "rgba(255, 255, 255, 0.25)"
                        },
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    },
                    datalabels: {
                        display: false
                    }
                }
            },
            data: {
                labels: ['Acústica', 'Dançante', 'Energética', 'Positiva', 'Triste'],
                datasets: [
                    {
                        label: 'Média',
                        data: [10, 80, 30, 40, 60],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        borderWidth: 1
                    }
                ]
            }
        }
    );
})();

(async function () {
    new Chart(
        musicalityChart,
        {
            type: 'line',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: {
                            color: "#fff"
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        ticks: {
                            color: "#fff",
                            callback: value => value + "%"
                        },
                        grid: {
                            color: "rgba(255, 255, 255, 0.25)"
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: {
                            color: '#fff',
                            font: {
                                size: 12
                            }
                        }
                    },
                    title: {
                        display: false
                    },
                    datalabels: {
                        display: false
                    }
                }
            },
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [
                    {
                        label: 'Acústica',
                        data: [10, 30, 10, 80, 20, 30, 100],
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        cubicInterpolationMode: 'monotone',
                        borderWidth: 1
                    },
                    {
                        label: 'Dançante',
                        data: [50, 20, 40, 60, 70, 80, 90],
                        fill: false,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        cubicInterpolationMode: 'monotone',
                        borderWidth: 1
                    },
                    {
                        label: 'Energética',
                        data: [30, 40, 60, 70, 80, 90, 100],
                        fill: false,
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        cubicInterpolationMode: 'monotone',
                        borderWidth: 1
                    },
                    {
                        label: 'Positiva',
                        data: [40, 60, 80, 100, 20, 10, 50],
                        fill: false,
                        borderColor: 'rgb(255, 206, 86)',
                        backgroundColor: 'rgba(255, 206, 86, 0.2)',
                        cubicInterpolationMode: 'monotone',
                        borderWidth: 1
                    },
                    {
                        label: 'Triste',
                        data: [70, 80, 90, 100, 50, 10, 80],
                        fill: false,
                        borderColor: 'rgb(153, 102, 255)',
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        cubicInterpolationMode: 'monotone',
                        borderWidth: 1
                    }
                ],
                borderWidth: 1
            }
        }
    );
})();

(async function () {
    mostListenedGenres = await fetch('/report/most-listened-genres')
        .then(response => response.json())
        .then(
            data => {
                if (data.error) {
                    console.error(data);
                    return;
                }

                return data;
            }
        );

    new Chart(
        genresChart,
        {
            type: 'radar',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        ticks: {
                            color: "rgba(255, 255, 255, 0.5)",
                            backdropColor: "rgba(0, 0, 0, 0)"
                        },
                        grid: {
                            color: "rgba(255, 255, 255, 0.25)"
                        },
                        pointLabels: {
                            color: "#fff"
                        }
                    },
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    },
                    datalabels: {
                        display: false
                    }
                }
            },
            data: {
                labels: mostListenedGenres.map(genre => getStringCapitalizedWords(genre[0])),
                datasets: [
                    {
                        label: 'Músicas',
                        data: mostListenedGenres.map(genre => genre[1]),
                        backgroundColor: 'rgba(94, 66, 252, 0.25)',
                        borderColor: 'rgba(94, 66, 252, 1)',
                        borderWidth: 1,
                        pointBackgroundColor: 'rgba(0, 0, 0, 0)',
                    }
                ]
                // labels: ['Electronic', 'Metal', 'Country', 'Classical', 'Jazz', 'Blues', 'Reggae', 'Folk', 'Punk', 'Soul'],
                // datasets: [{
                //     label: 'Músicas',
                //     data: [70, 80, 90, 100, 110, 120, 130, 140, 150, 160],
                //     backgroundColor: 'rgba(94, 66, 252, 0.25)',
                //     borderColor: 'rgba(94, 66, 252, 1)',
                //     borderWidth: 1,
                //     pointBackgroundColor: 'rgba(0, 0, 0, 0)',
                // }]
            },
        }
    )
})();