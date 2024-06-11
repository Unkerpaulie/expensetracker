// show password toggle
function showhide(ele) {
    const passwordToggle = document.getElementById("passwordToggle");
    const passwordField = document.getElementById(ele);
    if (passwordToggle.textContent == "SHOW") {
        passwordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        passwordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
}
