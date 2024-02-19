#!/usr/bin/node
const userId = getWithExpiry('newId');

//Load the available environments
async function getEnvironment(){
    return request.get('/environments')
    .then((envs) => {
        $("#community-select").html('')
        $.each(envs, function (index, env){
            $("#community-select").append('<option value="' + env.id + '">' + env.name + '</option>')
        })
    }).catch((err) => {
        errorHandler(err, "Could not load available environments");
    })
}

//Load all the available service categories
async function getCategories(){
    return request.get('/service-categories')
    .then((cats) => {
        $.each(cats, function (index, cat){
            $("#service-select").append('<option value="' + cat.id + '">' + cat.name + '</option>')
        })
    }).catch((err) => {
        errorHandler(err, "Error loading service categories");
    })
}

// Update the user category, avatar and location
async function putNewInfo(){
    $("#submit").on('click', function (){
        var ins = $("#profile-photo")[0].files.length;

        if(ins != 0) {
            var formData = new FormData();
            var file = $("#profile-photo")

            formData.append("file", file[0].files[0]);
            formData.append("fileName", userId);
            formData.append("folder", "user_avatar");

            var formpost = request.postFile(formData)
        } else {
            var formpost = null;
        }

        // create a service instance for the user
        var payload = JSON.stringify({
            "category_id": $("#service-select :selected").val(),
            "description": $("#descript-text").val(),
            "owner_id": userId,
        })
        var servicepost = request.post('/services', payload)
        var promArray = [servicepost]
        if (formpost != null) {
            promArray.push(formpost)
        }
        Promise.all(promArray).then((values) => {
            // var body = values[1];
            var service = values[0];
            setWithExpiry('serviceId', service.id);
            var payload = {
                "com_res": $("#community-select :selected").val(),
                "note": $('#descript-text').val(),
            }
            if (values.length === 2) {
                payload['avatar'] = values[1]
            }
            payload = JSON.stringify(payload);
            var endpoint = '/users/' + userId
            request.put(endpoint, payload)
            .then(() => {
                window.location.href = "image-upload-page.html";
            }).catch(() => {
                showAlert("Error encountered while updating profile image, please reload the page and try again", 'error');
            })
        }).catch((err) => {
            errorHandler(err, 'An error was encountered, please reload the page and try again');
        })
    })
}

Promise.all([getEnvironment(), getCategories(), putNewInfo()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Failed to load page");
})