const chartDiv = document.getElementById('chart');
const genresChart = document.getElementById('genres-chart')

(async function () {
    new Chart(
        chartDiv,
        {
            type: 'line',
            data: {
                labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
                datasets: [
                    {
                        label: 'Músicas ouvidas',
                        data: [10, 20, 30, 40, 50, 60],
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    },
                    {
                        label: 'Minutos ouvidos',
                        data: [20, 40, 60, 80, 100, 120],
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    },
                ],
            },
        }
    )
})();