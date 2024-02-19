#!/usr/bin/node
const userId = getWithExpiry('newId')


// Populate the page with the existing user info
async function getUserInfo() {
    return request.get('/user/profile')
    .then((user) => {
        $('#fname').val(user.first_name);
        $('#lname').val(user.last_name);
        $('#phone').val(user.phone_no);
        if (user.user_type === 'regular') {
            $("#descript-label").addClass('disappear');
            $("#descript-text").addClass('disappear');
        } else {
            $('#descript-text').val(user.note)
        }
        $("#prof-img").html("<img id='avatar' src='" + user.avatar + "'>")
        request.get('/environments')
        .then((envs) => {
            $.each(envs, function(index, env){
                if (user.com_res === env.id){
                    $('#community-select').append('<option value="' + env.id + '" selected>' + env.name + '</option>')
                } else {
                    $('#community-select').append('<option value="' + env.id + '">' + env.name + '</option>')
                }
            })
        })
    }).catch((err) => {
        errorHandler(err, "Could not load user info")
    })
}

// Update the user info
async function putInfo() {
    var avatar = false
    $('#profile-photo').on('change', function() {
        avatar = true
    })
    $('#submit').on('click', function(){
        var payload = {
            first_name: $('#fname').val(),
            last_name: $('#lname').val(),
            phone_no: $('#phone').val(),
            com_res: $('#community-select :selected').val(),
            note: $('#descript-text').val(),
        }
        var endpoint = '/users/' + userId;
        if (avatar === false) {
            payload =JSON.stringify(payload)
            return request.put(endpoint, payload)
            .then(() => {
                showAlert("Details updated successfully", 'success')
                getUserType()
            }).catch((err) => {
                errorHandler(err, "Could not update details, please try again")
            })
        } else {
            var formData = new FormData();
            var ins = $("#profile-photo")[0].files.length;
            if(ins == 0) {
                return;
            }
            var file = $("#profile-photo");
            formData.append("file", file[0].files[0]);
            formData.append("folder", "user_avatar");
            formData.append("fileName", userId);
            /*formData.append("folder", "user_avatar");
            formData.append('publicKey', 'public_YHk4EswEnK3KjAlQgpJBaxbP/FY=');*/

            return request.postFile(formData)
            .then((body) => {
                payload['avatar'] = body

                request.put(endpoint, JSON.stringify(payload))
                .then((data) => {
                    showAlert("Details updated successfully", 'success')
                    getUserType()
                }).catch((err) => {
                    errorHandler(err, "Could not update details, please try again")
                })
            })
        }
    })
}

Promise.all([getUserInfo(), putInfo()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Fail to load page");
})