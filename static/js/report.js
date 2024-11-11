const reportTypeForm = document.getElementById('report-type-form');
const recentlyPlayedContainer = document.getElementById('recently-played-container');
const recentlyPlayedSpinner = document.getElementById('recently-played-spinner');
const aiRecommendationContainer = document.getElementById('ai-recommendation-container');
const aiRecommendationSpinner = document.getElementById('ai-recommendation-spinner');
const trackComponent = document.getElementById('track-component');
const audioPlayer = document.getElementById('audio-player');

(async function getRecentlyPlayed() {
    recentlyPlayedSpinner.style.display = 'block';

    await fetch('/spotify/recently-played')
        .then(response => response.json())
        .then(
            data => {
                if (data.error) {
                    console.error(data);
                    recentlyPlayedContainer.innerHTML = `<p class="text-center text-white">Erro ao carregar músicas recentes</p><p class="text-center text-white">${JSON.stringify(data.error)}</p>`;
                    return;
                }

                data.items.forEach(item => {
                    const newTrackComponent = trackComponent.cloneNode(true);
                    newTrackComponent.style.display = 'block';
                    newTrackComponent.querySelector('#track-image').src = item.track.album.images[2].url;
                    newTrackComponent.querySelector('#track-image').alt = item.track.name;
                    newTrackComponent.querySelector('#track-name').textContent = item.track.name;
                    newTrackComponent.querySelector('#track-artist').textContent = item.track.artists[0].name;
                    recentlyPlayedContainer.appendChild(newTrackComponent);
                });
            },
            error => {
                console.error(error);
                recentlyPlayedContainer.innerHTML = `<p class="text-center text-white">Erro ao carregar músicas recentes</p><p class="text-center text-white">${JSON.stringify(error)}</p>`;
            }
        );

    recentlyPlayedSpinner.style.display = 'none';
})();

(async function getAiRecommendation() {
    aiRecommendationSpinner.style.display = 'block';

    if (localStorage.getItem('prediction')) {
        const data = JSON.parse(localStorage.getItem('prediction'));

        data.forEach(item => {
            const newTrackComponent = trackComponent.cloneNode(true);
            newTrackComponent.style.display = 'block';
            newTrackComponent.querySelector('#prediction-precision').textContent = item.similarity.toFixed(0) + "%";
            newTrackComponent.querySelector('#track-image').src = item['track_data'].album.images[2].url;
            newTrackComponent.querySelector('#track-image').alt = item['track_data'].name;
            newTrackComponent.querySelector('#track-name').textContent = item['track_data'].name;
            newTrackComponent.querySelector('#track-artist').textContent = item['track_data'].artists[0].name;

            if (item['track_data'].preview_url) {

                newTrackComponent.querySelector('#track-footer').style.display = 'block';

                const progressBar = newTrackComponent.querySelector('#audio-progress');

                audioPlayer.addEventListener('timeupdate', () => {
                    if (audioPlayer.src === item['track_data'].preview_url) {
                        progressBar.style.width = audioPlayer.currentTime / audioPlayer.duration * 100 + '%';
                    }
                    else {
                        progressBar.style.width = '0%';
                    }
                });

                newTrackComponent.querySelector('#audio-play').addEventListener('click', () => {
                    if (audioPlayer.src === item['track_data'].preview_url) {
                        if (audioPlayer.paused) {
                            audioPlayer.play();
                            newTrackComponent.querySelector('#audio-play').textContent = '⏸';
                        } else {
                            audioPlayer.pause();
                            newTrackComponent.querySelector('#audio-play').textContent = '▶';
                        }
                    } else {
                        audioPlayer.src = item['track_data'].preview_url;
                        audioPlayer.play();
                        newTrackComponent.querySelector('#audio-play').textContent = '⏸';
                    }
                });
            }

            aiRecommendationContainer.appendChild(newTrackComponent);
        });

        aiRecommendationSpinner.style.display = 'none';
        return;
    }

    await fetch('/prediction')
        .then(response => response.json())
        .then(
            data => {
                if (data.error) {
                    console.error(data);
                    aiRecommendationContainer.innerHTML = `<p class="text-center text-white">Erro ao carregar recomendação</p><p class="text-center text-white">${JSON.stringify(data.error)}</p>`;
                    return;
                }

                localStorage.setItem('prediction', JSON.stringify(data));

                data.forEach(item => {
                    const newTrackComponent = trackComponent.cloneNode(true);
                    newTrackComponent.style.display = 'block';
                    newTrackComponent.querySelector('#prediction-precision').textContent = item.similarity.toFixed(0) + "%";
                    newTrackComponent.querySelector('#track-image').src = item['track_data'].album.images[2].url;
                    newTrackComponent.querySelector('#track-image').alt = item['track_data'].name;
                    newTrackComponent.querySelector('#track-name').textContent = item['track_data'].name;
                    newTrackComponent.querySelector('#track-artist').textContent = item['track_data'].artists[0].name;
                    // newTrackComponent.querySelector('#audio-preview').src = item['track_data'].preview_url;
                    aiRecommendationContainer.appendChild(newTrackComponent);
                });
            },
            error => {
                console.error(error);
                aiRecommendationContainer.innerHTML = `<p class="text-center text-white">Erro ao carregar recomendação</p><p class="text-center text-white">${JSON.stringify(error)}</p>`;
            }
        );

    aiRecommendationSpinner.style.display = 'none';
})();

reportTypeForm.addEventListener('change', e => {
    if (e.target.id === 'recently-played') {
        recentlyPlayedContainer.style.display = 'flex';
        aiRecommendationContainer.style.display = 'none';
    } else {
        recentlyPlayedContainer.style.display = 'none';
        aiRecommendationContainer.style.display = 'flex';
    }
});