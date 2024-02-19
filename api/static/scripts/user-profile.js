#!/usr/bin/node
userId = getWithExpiry('newId');

// load the communities
async function getEnvironment(){
	return request.get('/environments')
	.then((envs) => {
		$.each(envs, function(index, env){
			$("#community-select").append('<option value="' + env.id + '">' + env.name + '</option>')
		});
	}).catch((err) => {
		errorHandler(err, "Could not load environments now, please try later");
	})
};

// upload user community
async function postEnvironment(){
	var img = false;
	$("#profile-photo").on('change', () => {
		img = true;
	})
	$("#submit").on('click', function() {
		var payload = {}
		payload["com_res"] = $("#community-select :selected").val();
		endpoint = '/users/' + userId;
		if (img === true) {
			var formData = new FormData();
			var file = $("#profile-photo")
			formData.append("file", file[0].files[0]);
			formData.append("fileName", userId);
			formData.append("folder", "user_avatar");

			return request.postFile(formData)
			.then((body) => {
				payload['avatar'] = body;
				payload = JSON.stringify(payload)
				request.put(endpoint, payload)
				.then(() => {
					window.location.href = 'signup-confirmpage.html'
				}).catch((err) => {
					errorHandler(err, "Could not upload details, please refresh and try again");
				})
			}).catch((err) => {
				errorHandler(err, "Profile image was unable to update, please try again later");
			})
		} else {
			return request.put(endpoint, JSON.stringify(payload))
			.then(() => {
				window.location.href = 'signup-confirmpage.html';
			}).catch((err) => {
				errorHandler(err, "Could not upload details, please refresh and try again");
			})
		}
	});
};

Promise.all([getEnvironment(), postEnvironment()])
.then(() => {
	var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
	errorHandler(err, "Failed to load page");
})