var showLength = 1;
var delay = 1000;
var hideAll = setTimeout(function() {}, 0);

document.addEventListener("DOMContentLoaded", function() {
    var passwordInput = document.getElementById("password");

    passwordInput.addEventListener("input", function() {

        // Change the visible string
        if (passwordInput.value.length > showLength) {
            passwordInput.value = passwordInput.value.substring(0, passwordInput.value.length - showLength).replace(/./g, "•") + passwordInput.value.substring(passwordInput.value.length - showLength, passwordInput.value.length);
        }

        // Set the timer
        clearTimeout(hideAll);
        hideAll = setTimeout(function() {
            passwordInput.value = passwordInput.value.replace(/./g, "•");
        }, delay);
    });
});