const characteristicsSpinner = document.getElementById('characteristics-spinner');
const characteristicsChart = document.getElementById('characteristics-chart');
const musicalitySpinner = document.getElementById('musicality-spinner');
const musicalityChart = document.getElementById('musicality-chart');
const genresSpinner = document.getElementById('genres-spinner');
const genresChart = document.getElementById('genres-chart');

Chart.register(ChartDataLabels);

const featureNames = {
    acousticness: 'Acústica',
    danceability: 'Dançante',
    energy: 'Energética',
    valence: 'Positiva',
    liveness: 'Ao Vivo',
    instrumentalness: 'Instrumental',
    speechiness: 'Falada'
};

(async function () {
    characteristicsSpinner.style.display = 'block';

    var mostPresentFeatures = await fetch('/report/most-present-features')
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
                labels: Object.keys(mostPresentFeatures).map(feature => getStringCapitalizedWords(featureNames[feature])),
                datasets: [
                    {
                        label: 'Média',
                        data: Object.values(mostPresentFeatures).map(value => value * 100),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(181, 255, 8, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(181, 255, 8, 1)'
                        ],
                        borderWidth: 1
                    }
                ]
            }
        }
    );

    characteristicsSpinner.style.display = 'none';
})();

(async function () {
    musicalitySpinner.style.display = 'block';

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

    musicalitySpinner.style.display = 'none';
})();

(async function () {
    genresSpinner.style.display = 'block';

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
                        backgroundColor: 'rgba(153, 102, 255, 0.25)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1,
                        pointBackgroundColor: 'rgba(0, 0, 0, 0)',
                    }
                ]
            },
        }
    )

    genresSpinner.style.display = 'none';
})();