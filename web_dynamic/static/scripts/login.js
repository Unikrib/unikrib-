#!/usr/bin/node
var error = getWithExpiry("error")
if (error != null) {
    showAlert(error, 'warning');
}

async function login() {
    $("#login").on('click', function() {
        var email = $('#username').val();
        var password = $('#input-pass').val();
        return request.signin(email, password)
        .then((user) => {
            showTimedAlert(user.message, 'success', 3000);
            setWithExpiry('newId', user.id);
            setWithExpiry('token', user.token);
            setWithExpiry('user_type', user.user_type);
            setWithExpiry('first_name', user.first_name);
            if (!user.signup_complete) {
                user_type = user.user_type
                if (user_type === "sp"){
                    window.location.href = "service-profile.html";
                } else if (user_type === "agent"){
                    window.location.href = "agent-profile.html";
                } else if (user_type === "vendor"){
                    window.location.href = "vendor-profile.html";
                } else {
                    window.location.href = "user-profile.html";
                }
            }
            var path = getWithExpiry("path");
            if (path != null) {
                window.location.href = path;
            } else {
                if (user.user_type === 'vendor') {
                    window.location.href = 'product-page.html';
                } else if (user.user_type === 'sp') {
                    window.location.href = 'service-page.html';
                } else {
                    window.location.href = 'Apartment-page.html';
                }
            }
        }).catch((err) => {
            errorHandler(err, "Could not log in")
        })
    })
}

Promise.all([login()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Failed to log in");
})
