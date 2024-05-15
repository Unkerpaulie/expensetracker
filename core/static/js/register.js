// username validation
const usernameField = document.getElementById("username");
const usernameFeedback = document.getElementById("username_feedback");
const usernameCheck = document.getElementById("username_check");

usernameField.addEventListener("keyup", (e) => {
    const usernameEntry = e.target.value;
    // clear styles by default, only add when invalid
    usernameField.classList.remove("is-invalid");
    usernameFeedback.style.display = "none";
    usernameFeedback.innerText = "";
    // show checking message while waiting for fetch response
    usernameCheck.style.display = "block";
    usernameCheck.textContent = `Checking...${usernameEntry}`;

    if (usernameEntry.length > 0) {
        fetch("/auth/username_val", {
            body: JSON.stringify({username: usernameEntry}),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data => {
            usernameCheck.style.display = "none";
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
const emailCheck = document.getElementById("email_check");

emailField.addEventListener("keyup", (e) => {
    const emailEntry = e.target.value;
    // clear styles by default, only add when invalid
    emailField.classList.remove("is-invalid");
    emailFeedback.style.display = "none";
    emailFeedback.innerText = "";
    // show checking message while waiting for fetch response
    emailCheck.style.display = "block";
    emailCheck.textContent = `Checking...${emailEntry}`;

    if (emailEntry.length > 0) {
        fetch("/auth/email_val", {
            body: JSON.stringify({email: emailEntry}),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data => {
            emailCheck.style.display = "none";
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
const password2Check = document.getElementById("password2_check");

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

// confirm passsword match
const passwordFeedback2 = document.getElementById("password2_feedback");

passwordField2.addEventListener("keyup", (e) => {
    passwordField2.classList.remove("is-invalid");
    passwordFeedback2.style.display = "none";
    passwordFeedback2.innerText = "";
    if (passwordField.value !== passwordField2.value) {
        passwordField2.classList.add("is-invalid");
        passwordFeedback2.style.display = "block";
        passwordFeedback2.innerText = "Passwords do not match";
    }
})
