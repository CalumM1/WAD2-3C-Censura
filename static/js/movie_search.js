document.addEventListener("DOMContentLoaded", function () {
    function searchMovies() {
        var query = document.getElementById("movie-search").value;
        if (query.length > 2) {
            fetch(searchMoviesUrl + "?query=" + encodeURIComponent(query)) 
                .then(response => response.json())
                .then(data => {
                    var resultsContainer = document.getElementById("search-results");
                    resultsContainer.innerHTML = "";
                    data.movies.forEach(movie => {
                        let listItem = document.createElement("li");
                        listItem.textContent = movie.name;
                        listItem.classList.add("search-result-item");
                        resultsContainer.appendChild(listItem);
                    });
                })
                .catch(error => console.error("Error fetching movies:", error));
        } else {
            document.getElementById("search-results").innerHTML = "";
        }
    }

    var searchBox = document.getElementById("movie-search");
    if (searchBox) {
        searchBox.addEventListener("keyup", searchMovies);
    }

    document.getElementById("search-results").addEventListener("click", function (event) {
        if (event.target.classList.contains("search-result-item")) {
            let movieName = event.target.textContent;
            alert("You liked: " + movieName);
        }
    });
});
