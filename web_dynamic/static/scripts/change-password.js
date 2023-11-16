#!/usr/bin/python3

$(function() {
    $("#update").on('click', function() {
        var passwd = $("#input-pass").val();
        var passwd2 = $("#input-pass2").val();
        var email = getWithExpiry("email");

        if (passwd === passwd2) {
            var payload = JSON.stringify({
                "password": passwd,
                "email": email,
            })
        } else {
            showAlert("Passwords did not match", 'warning');
            return;
        }

        url = '/users/email'
        request.put(url, payload)
        .then((user) => {
            showAlert("Password sucessfully changed", 'success');
            setWithExpiry("token", user.token)
            setWithExpiry("newId", user.id)
            setWithExpiry('first_name', user.first_name);
            if (user.user_type == 'vendor') {
                window.location.href = 'product-page.html';
            } else if (user.user_type == 'sp') {
                window.location.href = 'service-page.html';
            } else {
                window.location.href = 'Apartment-page.html';
            }
        }).catch((err) => {
            errorHandler(err, "Error updating password");
        })
    })
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})