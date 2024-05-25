document.addEventListener('DOMContentLoaded', function() {
    let currentPage = 1;

    function loadMedia(page) {
        fetch(`http://127.0.0.1:5000/get_videos?page=${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(medias => {
            const container = document.getElementById('video-container');
            container.innerHTML = ''; // Clear existing videos

            medias.forEach(media => {
                const mediaCard = document.createElement('div');
                mediaCard.classList.add('card1');

                const mediaLink = document.createElement('a');
                mediaLink.href = `video_detail.html?video=${media[0]}`;

                // Check the file extension to decide the element to create
                const url = media[1];
                if (url.match(/\.(jpeg|jpg|gif|png)$/)) { // For images and GIFs
                    const imgElement = document.createElement('img');
                    imgElement.src = url;
                    imgElement.style.width = '100%';
                    imgElement.style.height = '200px';
                    imgElement.style.objectFit = 'cover';
                    mediaLink.appendChild(imgElement);
                } else if (url.match(/\.(mp4|webm)$/)) { // For videos
                    const videoElement = document.createElement('video');
                    videoElement.src = url;
                    videoElement.controls = true;
                    videoElement.style.width = '100%';
                    videoElement.style.height = '200px';
                    videoElement.style.objectFit = 'cover';
                    mediaLink.appendChild(videoElement);
                }

                const cardInfo = document.createElement('div');
                cardInfo.classList.add('card-info');

                const publicationDate = document.createElement('p');
                publicationDate.textContent = `Date de publication: ${media.publication_date || 'undefined'}`;

                const artistName = document.createElement('p');
                artistName.textContent = `Artist: ${media.artist_name || 'undefined'}`;

                const animeTitle = document.createElement('p');
                animeTitle.textContent = `Anime: ${media.anime_title || 'undefined'}`;

                cardInfo.appendChild(publicationDate);
                cardInfo.appendChild(artistName);
                cardInfo.appendChild(animeTitle);

                mediaCard.appendChild(mediaLink);
                mediaCard.appendChild(cardInfo);
                container.appendChild(mediaCard);
            });
        })
        .catch(error => {
            console.error('Failed to fetch media:', error);
            alert('Failed to load media: ' + error.message);
        });
    }

    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadMedia(currentPage);
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        currentPage++;
        loadMedia(currentPage);
    });

    loadMedia(currentPage);
});
    


function fetchVideos() {
    fetch('http://127.0.0.1:5000/get_videos')
        .then(response => response.json())
        .then(data => {
            const videoContainer = document.getElementById('video-container');
            videoContainer.innerHTML = ''; // Clear existing videos
            data.forEach(video => {
                const videoCard = document.createElement('div');
                videoCard.classList.add('card1');

                const videoLink = document.createElement('a');
                videoLink.href = `video_detail.html?video=${video.anime_title}`;

                const videoElement = document.createElement('video');
                videoElement.src = video.url;
                videoElement.controls = true;

                const cardInfo = document.createElement('div');
                cardInfo.classList.add('card-info');

                const publicationDate = document.createElement('p');
                publicationDate.textContent = `Date de publication: ${video.publication_date}`;

                const artistName = document.createElement('p');
                artistName.textContent = `Artist: ${video.artiste_name}`;

                const animeTitle = document.createElement('p');
                animeTitle.textContent = `Anime: ${video.anime_title}`;

                cardInfo.appendChild(publicationDate);
                cardInfo.appendChild(artistName);
                cardInfo.appendChild(animeTitle);

                videoLink.appendChild(videoElement);
                videoLink.appendChild(cardInfo);

                videoCard.appendChild(videoLink);
                videoContainer.appendChild(videoCard);
            });
        })
        .catch(error => console.error('Error fetching videos:', error));
}
