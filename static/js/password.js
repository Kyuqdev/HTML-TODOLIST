var showLength = 1;
var delay = 1000;
var hideAll = setTimeout(function() {}, 0);

document.addEventListener("DOMContentLoaded", function() {
    var passwordInput = document.getElementById("password");
    var hiddenValue = document.getElementById("hidden-password");

    passwordInput.addEventListener("input", function() {
        var offset = document.getElementById("password").value.length - document.getElementById("hidden-password").innerHTML.length;
        if (offset > 0) {
            document.getElementById("hidden-password").innerHTML += document.getElementById("password").value.substring(document.getElementById("hidden-password").innerHTML.length, document.getElementById("hidden-password").innerHTML.length + offset);
        } else if (offset < 0) {
            document.getElementById("hidden-password").innerHTML = document.getElementById("hidden-password").innerHTML.substring(0, document.getElementById("hidden-password").innerHTML.length + offset);
        }
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