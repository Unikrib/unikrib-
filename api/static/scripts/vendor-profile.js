#!/usr/bin/node

// Load the available product categories
async function getCategories() {
    return request.get('/categories')
    .then((cats) => {
        $.each(cats, function(_index, cat) {
            $("#product-select").append(`<option value="` + cat.id + `">` + cat.name + `</option>`);
        })
    }).catch((err) => {
        errorHandler(err, 'Could not load categories, please refresh the page');
    })
}


// Load the availble environments
async function getEnvironment() {
    return request.get('/environments')
    .then((envs) => {
        $.each(envs, function(_index, env) {
            $("#community-select").append(`<option value="` + env.id + `">` + env.name + `</option>`);
        })
    }).catch((err) => {
        errorHandler(err, 'Could not load communities, please refresh the page');
    })
}

// Post user new details
async function postInfo() {
    const userId = getWithExpiry('newId');
    $("#submit-prof").on('click', () => {
        userDict = {
            com_res: $("#community-select :selected").val(),
            note: $("#descript-text").val(),
            category: $("#product-select :selected").val(),
        }

        var formData = new FormData();
        var endpoint = '/users/' + userId;
        var file = $("#profile-photo")
        var ins = $("#profile-photo")[0].files.length;
        if (ins === 0) {
            payload = JSON.stringify(userDict)
            request.put(endpoint, payload)
            .then(() => {
                showAlert("Your details have been uploaded succesfully", 'success');
                window.location.href = 'signup-confirmpage.html';
            }).catch((err) => {
                errorHandler(err, "An error has occured")
            })
        } else {

            formData.append("file", file[0].files[0]);
            formData.append("fileName", userId);
            formData.append("folder", "user_avatar");

            return request.postFile(formData)
            .then((body) => {
                userDict['avatar'] = body
                payload = JSON.stringify(userDict)
                request.put(endpoint, payload)
                .then(() => {
                    showAlert("Your details have been uploaded succesfully", 'success');
                    window.location.href = 'signup-confirmpage.html';
                }).catch((err) => {
                    errorHandler(err, "An error has occured")
                })
            })
        }
    })
}

Promise.all([getCategories(), getEnvironment(), postInfo()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Failed to load page");
})