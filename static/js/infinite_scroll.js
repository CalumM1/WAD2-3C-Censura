document.addEventListener('DOMContentLoaded', function () {
    let page = 2;  // Start from page 2
    let loading = false;
    let container = document.getElementById('infinite-scroll-container');
    let loadingIndicator = document.getElementById('loading');

    if (!container || !loadingIndicator) return;

    window.addEventListener('scroll', function () {
        if (loading) return;

        let scrollHeight = document.documentElement.scrollHeight;
        let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        let clientHeight = document.documentElement.clientHeight;

        if (scrollTop + clientHeight >= scrollHeight - 50) {  // Near bottom
            loading = true;
            loadingIndicator.style.display = 'block';

            fetch(window.location.pathname + `?page=${page}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(response => response.json())
                .then(data => {
                    if (data.items.length > 0) {
                        data.items.forEach(item => {
                            let div = document.createElement('div');
                            div.classList.add('review', 'scroll-item');
                            div.innerHTML = `
                                <div style="display: flex; justify-content: space-between;">
                                    <h4>${item.movie}</h4>
                                    <button class="like-review-btn" data-review-id="">
                                        <span class="thumb">
                                            👍 <span class="like-count">${item.likes_count}</span>
                                        </span>
                                    </button>
                                </div>
                                <p>Rating: ${item.rating}/10</p>
                                <p>${item.text}</p>
                                <a href="${item.url}">See Thread</a>
                                <p class="review-date">${item.created_at}</p>
                            `;
                            container.appendChild(div);
                        });

                        page++;
                        loading = false;
                    }

                    if (!data.has_next) {
                        window.removeEventListener('scroll', arguments.callee);
                    }

                    loadingIndicator.style.display = 'none';
                })
                .catch(error => {
                    console.error("Error fetching reviews:", error);
                    loading = false;
                    loadingIndicator.style.display = 'none';
                });
        }
    });
});
