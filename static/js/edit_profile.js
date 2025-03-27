// edit_profile.js
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("movie-search");
    if (searchInput) {
        searchInput.addEventListener("keyup", searchMovies);
    }
});

function searchMovies() {
    const query = document.getElementById('movie-search').value;
    const resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '';

    if (query.length === 0) return;

    fetch(`${window.searchMoviesUrl}?query=${query}`)
        .then(response => response.json())
        .then(data => {
            data.movies.forEach(movie => {
                const li = document.createElement('li');
                li.textContent = movie.name;
                li.className = 'list-group-item list-group-item-action';
                li.style.color = 'black';
                li.style.cursor = 'pointer';
                li.onclick = () => toggleLike(movie.slug, movie.name);
                resultsContainer.appendChild(li);
            });
        });
}

function toggleLike(slug, displayName) {
    fetch(`/censura/movies/${slug}/toggle-favourite/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (!data.is_favourite) {
                    const tag = document.querySelector(`[data-movie-slug="${slug}"]`);
                    if (tag) tag.remove();
                } else {
                    const existingTag = document.querySelector(`[data-movie-slug="${slug}"]`);
                    if (existingTag) return; // already in the DOM
                
                    const likedMoviesContainer = document.getElementById('liked-movies-container');
                    const newTag = document.createElement('div');
                    newTag.className = 'movie-tag';
                    newTag.dataset.movieSlug = slug;
                    newTag.style = 'background-color: #444; padding: 5px 10px; border-radius: 20px; display: flex; align-items: center;';
                    newTag.innerHTML = `
                        <span>${displayName}</span>
                        <button onclick="toggleLike('${slug}', '${displayName}')" style="background: none; border: none; margin-left: 8px; font-weight: bold; cursor: pointer;">&times;</button>
                    `;
                    likedMoviesContainer.appendChild(newTag);
                }
                
            }
        });
}
