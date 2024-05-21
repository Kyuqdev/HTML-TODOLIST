function attemptLogin() {
    //* get the values from the username and password fields
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    //* create a json object with the username and password
    let loginData = {
        username: username,
        password: password
    };

    //* send a post request to the server with the login data
    fetch('/account/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },

        //* stringify the json object and send it as the body of the request
        body: JSON.stringify(loginData)
    }).then(res => {
        res.text().then(responseText => {
            console.log(responseText);

            //* if the response is 200, set the token cookie to the response token
            if (res.status === 200) {

            //* set the token cookie to the response token with a max age of 1 day, then reload the page
            document.cookie = `token=${responseText}; max-age=86400`;
            window.location.reload();
            } else {

            //* if the response is not 200, alert the user with the server response message
            alert(responseText);
            }
        });
    });
}

document.getElementById("submit").addEventListener('click', function() {
    attemptLogin();
});