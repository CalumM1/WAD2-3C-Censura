document.addEventListener("DOMContentLoaded", function() {
    const sortDropdown = document.getElementById("sort");
    const reviewsContainer = document.getElementById("all-reviews-container");
    const movieSlug = reviewsContainer.dataset.movieSlug; // Movie slug from data attribute

    sortDropdown.addEventListener("change", function() {
        const sortBy = this.value; // Get selected sort option

        // Fetch sorted reviews from the Django view
        fetch(`/censura/movies/${movieSlug}/sorted-reviews/?sort=${sortBy}`)
            .then(response => response.json())
            .then(data => {
                reviewsContainer.innerHTML = "";

                if (data.reviews.length > 0) {
                    // Create a container for new reviews
                    const movieReviewsDiv = document.createElement("div");
                    movieReviewsDiv.classList.add("movie-reviews");

                    data.reviews.forEach(review => {
                        // Dynamically create the correct review URL
                        const reviewUrl = `/censura/movies/${movieSlug}/review/${review.user}`;

                        // Build the review element
                        const reviewElement = document.createElement("div");
                        reviewElement.classList.add("review");
                        reviewElement.innerHTML = `
                            <h4>Reviewed by ${review.user}</h4>
                            <p>Rating: ${review.rating}/10</p>
                            <p>${review.text}</p>
                            <a href="${reviewUrl}">Read More</a>
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
