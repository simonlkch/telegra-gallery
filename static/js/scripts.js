document.addEventListener('DOMContentLoaded', function() {
  // Dark Mode Toggle
  document.getElementById('darkModeToggle').addEventListener('click', function() {
    var body = document.body;
    var navbar = document.querySelector('.navbar');
    var button = document.getElementById('darkModeToggle');
    if (body.classList.contains('light-mode')) {
      body.classList.remove('light-mode');
      body.classList.add('dark-mode');
      navbar.classList.remove('navbar-light');
      navbar.classList.add('navbar-dark');
      button.classList.remove('btn-light-mode');
      button.classList.add('btn-dark-mode');
      button.textContent = 'Light Mode';
    } else {
      body.classList.remove('dark-mode');
      body.classList.add('light-mode');
      navbar.classList.remove('navbar-dark');
      navbar.classList.add('navbar-light');
      button.classList.remove('btn-dark-mode');
      button.classList.add('btn-light-mode');
      button.textContent = 'Dark Mode';
    }
  });

  // Upload Form Submission with Progress Bar
  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/', true);

    xhr.upload.onprogress = function(event) {
      if (event.lengthComputable) {
        var percentComplete = (event.loaded / event.total) * 100;
        var progressBar = document.getElementById('progressBar');
        progressBar.style.width = percentComplete + '%';
        progressBar.setAttribute('aria-valuenow', percentComplete);
        progressBar.innerHTML = Math.round(percentComplete) + '%';
      }
    };

    xhr.onload = function() {
      if (xhr.status === 200) {
        var accessToken = document.getElementById('access_token').value;
        localStorage.setItem('access_token', accessToken);
        document.getElementById('createdPagesLink').click();
      } else {
        alert('Upload failed');
      }
    };

    xhr.send(formData);
  });

  // Redirect to created pages
  document.getElementById('createdPagesLink').addEventListener('click', function() {
    var accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      window.location.href = '/pages?access_token=' + accessToken;
    } else {
      alert('Please enter an access token first.');
    }
  });
});
