#!/usr/bin/node

$(function() {
    $('#reset').on('click', function() {
        var email = $('#username').val();

        url = '/users/reset-password';
        data = JSON.stringify({"email": email})
        request.post(url, data)
        .then(() => {
            setWithExpiry("email", email)
            window.location.href = 'reset-password.html';
        }).catch((err) => {
            errorHandler(err, "Service unavailable, please try again later");
        })
    })
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})