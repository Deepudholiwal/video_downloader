function showProgressBar() {
    document.getElementById('progress-bar-container').style.display = 'block';
}

function hideProgressBar() {
    document.getElementById('progress-bar-container').style.display = 'none';
}

function updateProgressBar(percentage) {
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = percentage + '%';
    progressBar.innerText = percentage + '%';
}

function downloadVideo() {
    const url = document.getElementById('url').value.trim();
    const messageElement = document.getElementById('message');
    
    if (!url) {
        messageElement.innerText = 'Please provide a link!';
        return;
    }

    const csrftoken = getCookie('csrftoken');
    showProgressBar();

    const formData = new FormData();
    formData.append('url', url);

    fetch('/download/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        hideProgressBar();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'video.mp4'; // You can customize this filename
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

        messageElement.innerText = 'Download completed!';
    })
    .catch(error => {
        hideProgressBar();
        messageElement.innerText = 'An error occurred: ' + error;
    });

    // Simulate progress for demonstration
    let progress = 0;
    const interval = setInterval(() => {
        if (progress >= 100) {
            clearInterval(interval);
        } else {
            progress += 10;
            updateProgressBar(progress);
        }
    }, 500);
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
