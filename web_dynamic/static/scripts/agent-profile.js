#!/usr/bin/node
const userId = getWithExpiry('newId');

// Load all the available environments
async function getEnvironment() {
    return request.get('/environments')
    .then((envs) => {
        $.each(envs, function(index, env){
            $('#community-select').append('<option value="' + env.id + '">' + env.name + '</option>')
        })
    })
}

// Update the user info and image
async function putInfo() {
    $('#submit').on('click', function() {
        var com_res = $('#community-select :selected').val();
        if (com_res === '') {
            showAlert('Please select a community of residence', 'error')
        }
        userDict = {
            note: $('#descript-text').val(),
            com_res: com_res,
        }
        endpoint = '/users/' + userId;

        var formData = new FormData();        
        var file = $("#profile-photo");
        var ins = $("#profile-photo")[0].files.length;
        if (ins === 0) {
            payload = JSON.stringify(userDict)
            request.put(endpoint, payload)
            .then(() => {
                showAlert("Your details have been uploaded succesfully", 'success');
                window.location.href = 'signup-confirmpage.html';
            }).catch((err) => {
                errorHandler(err, "Error encountered while uploading details")
            })
        } else {
            formData.append("file", file[0].files[0]);
            formData.append("fileName", userId);
            formData.append("folder", "user_avatar");

            return request.postFile(formData)
            .then((body) => {
                userDict["avatar"] = body;
                payload = JSON.stringify(userDict)
                
                request.put(endpoint, payload)
                .then(() => {
                    showAlert("Your details have been uploaded succesfully", 'success');
                    window.location.href = 'signup-confirmpage.html';
                }).catch((err) => {
                    errorHandler(err, "Error encountered while uploading details");
                })
            }).catch((err) => {
                errorHandler(err, "Error encountered while uploading profile avatar");
            })
        }
    })
}

Promise.all([getEnvironment(), putInfo()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
}).catch((err) => {
    errorHandler(err, "Failed to load page");
})