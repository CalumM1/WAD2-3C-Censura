document.addEventListener("DOMContentLoaded", function() {
    const sortDropdown = document.getElementById("sort");
    const reviewsContainer = document.getElementsByClassName("review-section")[1];
    const movieSlug = reviewsContainer.dataset.movieSlug;

    sortDropdown.addEventListener("change", function() {
        const sortBy = this.value;
        console.log(movieSlug);

        fetch(`/censura/movies/${movieSlug}/sorted-reviews/?sort=${sortBy}`)
            .then(response => response.json())
            .then(data => {
                reviewsContainer.innerHTML = "";
                
                if (data.reviews.length > 0) {

                    const movieReviewsDiv = document.createElement("div");
                    movieReviewsDiv.classList.add("movie-reviews");
                    
                    data.reviews.forEach(review => {
                        const reviewElement = document.createElement("div");
                        reviewElement.classList.add("review");
                        reviewElement.innerHTML = `
                            <h4>Reviewed by ${review.user}</h4>
                            <p>Rating: ${review.rating}/10</p>
                            <p>${review.text}</p>
                            <p class="review-date">${review.created_at}</p>
                        `;
                        movieReviewsDiv.appendChild(reviewElement);
                    });
                    
                    reviewsContainer.appendChild(movieReviewsDiv);
                } else {
                    reviewsContainer.innerHTML = "<p>No reviews yet. Be the first to review!</p>";
                }
            })
            .catch(error => console.error("Error fetching reviews:", error));
    });
});