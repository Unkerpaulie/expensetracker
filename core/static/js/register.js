const usernameField = document.getElementById("username");
const usernameFeedback = document.getElementById("username_feedback");

usernameField.addEventListener("keyup", (e) => {
    const usernameEntry = e.target.value;
    // set up dynamic route call
    if (usernameEntry.length > 0) {
        fetch("/auth/username_val", {
            body: JSON.stringify({username: usernameEntry}),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data => {
            console.log("data", data);
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                usernameFeedback.style.display = "block";
                usernameFeedback.innerText = data.username_error;
            }
            if (data.username_valid) {
                usernameField.classList.remove("is-invalid");
                usernameFeedback.style.display = "none";
                usernameFeedback.innerText = "";
            }
            console.log("display", usernameFeedback.innerText);
            
        }));
    }
})