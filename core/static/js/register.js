// username validation
const usernameField = document.getElementById("username");
const usernameFeedback = document.getElementById("username_feedback");

usernameField.addEventListener("keyup", (e) => {
    const usernameEntry = e.target.value;
    // clear styles by default, only add when invalid
    usernameField.classList.remove("is-invalid");
    usernameFeedback.style.display = "none";
    usernameFeedback.innerText = "";

    if (usernameEntry.length > 0) {
        fetch("/auth/username_val", {
            body: JSON.stringify({username: usernameEntry}),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data => {
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                usernameFeedback.style.display = "block";
                usernameFeedback.innerText = data.username_error;
            }
        }));
    }
})

// email validation
const emailField = document.getElementById("email");
const emailFeedback = document.getElementById("email_feedback");

emailField.addEventListener("keyup", (e) => {
    const emailEntry = e.target.value;
    // clear styles by default, only add when invalid
    emailField.classList.remove("is-invalid");
    emailFeedback.style.display = "none";
    emailFeedback.innerText = "";

    if (emailEntry.length > 0) {
        fetch("/auth/email_val", {
            body: JSON.stringify({email: emailEntry}),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data => {
            if (data.email_error) {
                emailField.classList.add("is-invalid");
                emailFeedback.style.display = "block";
                emailFeedback.innerText = data.email_error;
            }
        }));
    } 
})

// show password toggle
const passwordToggle = document.getElementById("passwordToggle");
const passwordField = document.getElementById("password");
const passwordField2 = document.getElementById("password2");

passwordToggle.addEventListener("click", (e) => {
    if (passwordToggle.textContent == "SHOW") {
        passwordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
        passwordField2.setAttribute("type", "text");
    } else {
        passwordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
        passwordField2.setAttribute("type", "password"); 
    }
})