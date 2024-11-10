const reportTypeForm = document.getElementById('report-type-form');
const recentlyPlayedContainer = document.getElementById('recently-played-container');
const aiRecommendationContainer = document.getElementById('ai-recommendation-container');
const trackComponent = document.getElementById('track-component');

if (localStorage.getItem('recentlyPlayed')) {
    const recentlyPlayed = JSON.parse(localStorage.getItem('recentlyPlayed'));
    recentlyPlayed.forEach(item => {
        const newTrackComponent = trackComponent.cloneNode(true);
        newTrackComponent.style.display = 'block';
        newTrackComponent.querySelector('#track-image').src = item.track.album.images[2].url;
        newTrackComponent.querySelector('#track-image').alt = item.track.name;
        newTrackComponent.querySelector('#track-name').textContent = item.track.name;
        newTrackComponent.querySelector('#track-artist').textContent = item.track.artists[0].name;
        recentlyPlayedContainer.appendChild(newTrackComponent);
    });
} else {
    fetch('/spotify/recently-played')
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('recentlyPlayed', JSON.stringify(data.items));

            data.items.forEach(item => {
                const newTrackComponent = trackComponent.cloneNode(true);
                newTrackComponent.style.display = 'block';
                newTrackComponent.querySelector('#track-image').src = item.track.album.images[2].url;
                newTrackComponent.querySelector('#track-image').alt = item.track.name;
                newTrackComponent.querySelector('#track-name').textContent = item.track.name;
                newTrackComponent.querySelector('#track-artist').textContent = item.track.artists[0].name;
                recentlyPlayedContainer.appendChild(newTrackComponent);
            });
        });
}

if (localStorage.getItem('aiRecommendation')) {
    const aiRecommendation = JSON.parse(localStorage.getItem('aiRecommendation'));
    aiRecommendation.forEach(item => {
        const newTrackComponent = trackComponent.cloneNode(true);
        newTrackComponent.style.display = 'block';
        newTrackComponent.querySelector('#prediction-precision').textContent = item.similarity.toFixed(4);
        newTrackComponent.querySelector('#track-image').src = item['track_data'].album.images[2].url;
        newTrackComponent.querySelector('#track-image').alt = item['track_data'].name;
        newTrackComponent.querySelector('#track-name').textContent = item['track_data'].name;
        newTrackComponent.querySelector('#track-artist').textContent = item['track_data'].artists[0].name;
        aiRecommendationContainer.appendChild(newTrackComponent);
    });
} else {
fetch('/prediction')
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('aiRecommendation', JSON.stringify(data));
        data.forEach(item => {
            const newTrackComponent = trackComponent.cloneNode(true);
            newTrackComponent.style.display = 'block';
            newTrackComponent.querySelector('#prediction-precision').textContent = item.similarity.toFixed(4);
            newTrackComponent.querySelector('#track-image').src = item['track_data'].album.images[2].url;
            newTrackComponent.querySelector('#track-image').alt = item['track_data'].name;
            newTrackComponent.querySelector('#track-name').textContent = item['track_data'].name;
            newTrackComponent.querySelector('#track-artist').textContent = item['track_data'].artists[0].name;
            aiRecommendationContainer.appendChild(newTrackComponent);
        });
    });
}

reportTypeForm.addEventListener('change', e => {
    if (e.target.id === 'recently-played') {
        recentlyPlayedContainer.style.display = 'flex';
        aiRecommendationContainer.style.display = 'none';
    } else {
        recentlyPlayedContainer.style.display = 'none';
        aiRecommendationContainer.style.display = 'flex';
    }
});