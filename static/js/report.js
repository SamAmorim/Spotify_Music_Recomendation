const reportTypeForm = document.getElementById('report-type-form');
const tableContainer = document.getElementById('table-container');

const recentlyPlayedTable = document.createElement('table');
recentlyPlayedTable.className = 'table table-striped table-hover';

const aiRecommendationTable = document.createElement('table');
aiRecommendationTable.className = 'table table-striped table-hover';

const recentlyPlayedThead = document.createElement('thead');
recentlyPlayedThead.innerHTML = '<tr><th></th><th>Música</th><th>Artista</th></tr>';
recentlyPlayedTable.appendChild(recentlyPlayedThead);

const aiRecommendationThead = document.createElement('thead');
aiRecommendationThead.innerHTML = '<tr><th></th><th>Música</th><th>Artista</th></tr>';
aiRecommendationTable.appendChild(aiRecommendationThead);

const recentlyPlayedTbody = document.createElement('tbody');
recentlyPlayedTable.appendChild(recentlyPlayedTbody);

const aiRecommendationTbody = document.createElement('tbody');
aiRecommendationTable.appendChild(aiRecommendationTbody);

tableContainer.appendChild(recentlyPlayedTable);
tableContainer.appendChild(aiRecommendationTable);

fetch('/spotify/recently-played')
    .then(response => response.json())
    .then(data => {
        data.items.forEach(item => {
            const tr = document.createElement('tr');

            const imgCell = document.createElement('td');
            const img = document.createElement('img');
            img.src = item.track.album.images[2].url;
            img.alt = item.track.name;
            img.style.width = '50px';
            img.style.height = '50px';
            imgCell.appendChild(img);
            tr.appendChild(imgCell);

            const trackCell = document.createElement('td');
            trackCell.textContent = item.track.name;
            tr.appendChild(trackCell);

            const artistCell = document.createElement('td');
            artistCell.textContent = item.track.artists[0].name;
            tr.appendChild(artistCell);

            recentlyPlayedTbody.appendChild(tr);
        });
    });

reportTypeForm.addEventListener('change', e => {
    if (e.target.id === 'recently-played') {
        recentlyPlayedTable.style.display = 'table';
        aiRecommendationTable.style.display = 'none';
    } else {
        recentlyPlayedTable.style.display = 'none';
        aiRecommendationTable.style.display = 'table';
    }
});