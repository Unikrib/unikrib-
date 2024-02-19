#!/usr/bin/node

// Post the user details
async function postDetail(){
	var $first_name = $("#first_name");
	var $last_name = $("#last_name");
	var $email = $("#email");
	var $phone_no = $("#phone_no");
	var $password = $("#input-pass");

	$("#submit").on('click', function() {
		var user_type = $("#account-type-input :selected").val()
		var payload = JSON.stringify({
			"first_name": $first_name.val(),
			"last_name": $last_name.val(),
			"email": $email.val(),
			"phone_no": $phone_no.val(),
			"password": $password.val(),
			"user_type": user_type
		});

		return request.post('/users', payload)
		.then((new_dict) => {
			setWithExpiry('token', new_dict.token);
			setWithExpiry('newId', new_dict.id);
			setWithExpiry('first_name', new_dict.first_name)
			setWithExpiry('user_type', user_type);
			if (user_type === "sp"){
				window.location.href = "service-profile.html";
			} else if (user_type === "agent"){
				window.location.href = "agent-profile.html";
			} else if (user_type === "vendor"){
				window.location.href = "vendor-profile.html";
			} else {
				window.location.href = "user-profile.html";
			}
		}).catch((err) => {
			if (err.statusCode == 502 || err.statusCode == 500) {
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
						if (user_type === "sp"){
							window.location.href = "service-profile.html";
						} else if (user_type === "agent"){
							window.location.href = "agent-profile.html";
						} else if (user_type === "vendor"){
							window.location.href = "vendor-profile.html";
						} else {
							window.location.href = "user-profile.html";
						}
					})
				})
			} else {
				errorHandler(err, "Error");
			}
		})
	});
};

Promise.all([postDetail()])
.then(() => {
	var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
}).catch((err) => {
	errorHandler(err, "Failed to sign in");
})
