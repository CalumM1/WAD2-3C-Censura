document.addEventListener("DOMContentLoaded", function() {
    const sortDropdown = document.getElementById("sort");
    const reviewsContainer = document.getElementById("all-reviews-container");
    const movieSlug = reviewsContainer.dataset.movieSlug;
    const allReviewsDiv = document.getElementById("all-reviews");

    sortDropdown.addEventListener("change", function() {
        const sortBy = this.value;

        fetch(`/censura/movies/${movieSlug}/sorted-reviews/?sort=${sortBy}`)
            .then(response => response.json())
            .then(data => {
                // Clear existing reviews
                allReviewsDiv.innerHTML = "";

                if (data.reviews.length > 0) {
                    data.reviews.forEach(review => {
                        // Dynamically create the correct review URL
                        const reviewUrl = `/censura/movies/${movieSlug}/review/${review.user}`;


                        const reviewDiv = document.createElement("div");
                        reviewDiv.classList.add("review");
                        reviewDiv.setAttribute("data-review-url", reviewUrl);


                        const isAuthenticated = document.body.dataset.isAuthenticated === 'true';


                        reviewDiv.innerHTML = `
                            <h4>Reviewed by <a href="/censura/my_account/${review.user}">${review.user}</a></h4>
                            <p>Rating: ${review.rating}/10</p>
                            <p>${review.text}</p>
                            
                            ${isAuthenticated ? `
                            <button class="like-review-btn" data-review-id="">
                                <span class="thumb">
                                    👍 <span class="like-count">${review.likes_count}</span>
                                </span>
                            </button>
                            ` : ''}
                            
                            <a href="${reviewUrl}">Read More</a>
                            <p class="review-date">${review.created_at}</p>
                        `;

                        // Append to reviews container
                        allReviewsDiv.appendChild(reviewDiv);
                    });
                } else {
                    allReviewsDiv.innerHTML = "<p class='text-center'>No reviews yet. Be the first to review!</p>";
                }
            })
            .catch(error => console.error("Error fetching reviews:", error));
    });
});