function login(event) {
    // Prevent form from submitting and refreshing the page
    event.preventDefault();

    // Get the username and password values from the input fields
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Predefined credentials (example credentials, you can change them)
    const validUsername = "jspm";  // Example username
    const validPassword = "jspm";  // Example password

    // Check if entered credentials match the predefined ones
    if (username === validUsername && password === validPassword) {
        // Redirect to the home page (index.html)
        window.location.href = "index.html";
    } else {
        // Display an alert if credentials are incorrect
        alert("Invalid username or password");
    }
}
