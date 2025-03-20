document.addEventListener('DOMContentLoaded', function () {
    let page = 2;  // Start from page 2
    let loading = false;
    let container = document.getElementById('infinite-scroll-container');
    let loadingIndicator = document.getElementById('loading');

    if (!container || !loadingIndicator) return;  // Exit if no container found

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
                            div.classList.add('scroll-item');

                            if (item.type === 'movie') {  // If it's a movie (favourites)
                                div.innerHTML = `
                                    <img src="${item.image}" alt="${item.name}">
                                    <h4>${item.name}</h4>
                                    <p>Directed by: ${item.director}</p>
                                    <p>Released: ${item.release_date}</p>
                                `;
                            } else if (item.type === 'review') {  // If it's a review
                                div.innerHTML = `
                                    <h4>${item.movie}</h4>
                                    <p>Rating: ${item.rating}/10</p>
                                    <p>${item.text}</p>
                                `;
                            }

                            container.appendChild(div);
                        });

                        page++;
                        loading = false;
                    }

                    if (!data.has_next) {
                        window.removeEventListener('scroll', arguments.callee);
                    }

                    loadingIndicator.style.display = 'none';
                });
        }
    });
});
