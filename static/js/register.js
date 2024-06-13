// username validation
const usernameField = document.getElementById("username");
const usernameFeedback = document.getElementById("username_feedback");
const usernameCheck = document.getElementById("username_check");

const submitBtn = document.getElementById("submit");
var valid_fields = new Set();

function allowSubmit() {
    // console.log("valid fields:", Array.from(valid_fields).join(', '));
    if (valid_fields.size >= 4) {
        submitBtn.removeAttribute("disabled");
    } else {
        submitBtn.disabled = true;
    }
}


// initialize disabled submit button
allowSubmit();

usernameField.addEventListener("keyup", (e) => {
    const usernameEntry = e.target.value;
    // clear styles by default, only add when invalid
    usernameField.classList.remove("is-invalid");
    usernameFeedback.style.display = "none";
    usernameFeedback.innerText = "";
    valid_fields.add("username");
    // show checking message while waiting for fetch response
    usernameCheck.style.display = "block";
    usernameCheck.textContent = `Checking... ${usernameEntry}`;

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
                valid_fields.delete("username");
                console.log("bad username");
            }
        })).then((whatever) => allowSubmit());
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
    valid_fields.add("email");
    // show checking message while waiting for fetch response
    emailCheck.style.display = "block";
    emailCheck.textContent = `Checking... ${emailEntry}`;

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
                valid_fields.delete("email");
            }
        })).then((whatever) => allowSubmit());
    } 
})



// check password length
const passwordField = document.getElementById("password");
const passwordFeedback = document.getElementById("password_feedback");

passwordField.addEventListener("keyup", (e) => {
    passwordField.classList.remove("is-invalid");
    passwordFeedback.style.display = "none";
    passwordFeedback.innerText = "";
    valid_fields.add("password");
    if (passwordField.value.length < 8) {
        passwordField.classList.add("is-invalid");
        passwordFeedback.style.display = "block";
        passwordFeedback.innerText = "Password must contain at least 8 characters";
        valid_fields.delete("password");
    }
    allowSubmit();
})

// confirm passsword match
const passwordField2 = document.getElementById("password2");
const passwordFeedback2 = document.getElementById("password2_feedback");

passwordField2.addEventListener("keyup", (e) => {
    passwordField2.classList.remove("is-invalid");
    passwordFeedback2.style.display = "none";
    passwordFeedback2.innerText = "";
    valid_fields.add("password2");
    if (passwordField.value !== passwordField2.value) {
        passwordField2.classList.add("is-invalid");
        passwordFeedback2.style.display = "block";
        passwordFeedback2.innerText = "Passwords do not match";
        valid_fields.delete("password2");
    }
    allowSubmit();
})
