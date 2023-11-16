#!/usr/bin/node

$(function() {
    var $firstname = $("#first_name");
    var $lastname = $("#last_name");
    var $email = $('#email');
    var $phone_no = $("#phone_no");
    var $password = $('#input-pass');

    $("#submit").on('click', function () {
        var payload = JSON.stringify({
            "first_name": $firstname.val(),
            "last_name": $lastname.val(),
            "email": $email.val(),
            "phone_no": $phone_no.val(),
            "password": $password.val(),
            "user_type": "regular",
        })

        request.post('/users', payload)
        .then((new_user) => {
            // alert(new_user.message);
    	    setWithExpiry('token', new_user.token);
            setWithExpiry('newId', new_user.id);
            setWithExpiry('first_name', new_user.first_name)
	    	window.location.href = "user-profile.html"
        }).catch((err) => {
            if (err.statusCode === 502 || err.statusCode === 500) {
				console.log("Creation failed on first attempt")
				dic = JSON.stringify({"email": $email.val()})
				request.delete('/users/current', dic)		// Delete any incomplete account that might have been created
				.then(() => {
					console.log("retrying...")
					request.post('/users', payload)		// Try to create another account
					.then((new_dict) => {
						setWithExpiry('token', new_dict.token);
						setWithExpiry('newId', new_dict.id);
                        setWithExpiry('first_name', new_dict.first_name)
						window.location.href = "Apartment-page.html";
					})
				})
			} else {
				errorHandler(err, "Could not create user, please try again");
			}
        })
    })
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
