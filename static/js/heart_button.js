function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("Button clicked!");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    document.querySelectorAll(".favourite-btn").forEach(button => {
        button.addEventListener("click", function () {
            const movieSlug = document.querySelector('.favourite-btn').getAttribute('data-movie-slug');

            fetch(`/censura/movies/${movieSlug}/toggle-favourite/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ movieSlug: movieSlug })
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_favourite) {
                    button.querySelector('span').classList.add('filled');
                    button.querySelector('span').classList.remove('empty');
                    button.querySelector('span').innerText = '❤️';
                } else {
                    button.querySelector('span').classList.add('empty');
                    button.querySelector('span').classList.remove('filled');
                    button.querySelector('span').innerText = '♡';
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
