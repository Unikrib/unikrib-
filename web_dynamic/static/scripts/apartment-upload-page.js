#!/usr/bin/node

const userId = getWithExpiry('newId');

// Load all environments
async function getEnvironment() {
    return request.get('/environments')
    .then((items) => {
        $.each(items, function (index, environment){
            $("#community").append('<option value="' + environment.id + '">' + environment.name + '</option>');
        })
    }).catch((err) => {
        errorHandler(err, "Error loading the environments")
    })
}

// Load the streets in the selected environment
async function getStreet() {
    $('#community').on('change', function() {
        const env_id = $("#community :selected").val();
        return request.get('/environments/' + env_id + '/streets')
        .then((streets) => {
            $('#street').html('');
                $.each(streets, function(index, street) {
                    $("#street").append('<option value="' + street.id + '">' + street.name + '</option>');
                })
        }).catch((err) => {
            errorHandler(err, "Could not load the streets in this environment, please reload the page")
        })
    })
}

// Post the inputted apartment details
async function postApartment(){
    $("#daily_power").text(12);
    $("#submit-apart").on('click', function(){
        var houseDict = {
            "apartment": $('#apartment :selected').val(),
            "name": $('#name').val(),
            "street_id": $("#street").val(),
            "price": $('#price').val(),
            "agent_fee": $("#agent-fee").val(),
            "running_water": $('#running-water :selected').val(),
            "waste_disposal": $('#adequate-disposal :selected').val(),
            "owner_id": userId,
            "features": $("#apart-descript").val(),
            "newly_built": $("#newly_built :selected").val(),
            "tiled": $("#tiled :selected").val(),
            "daily_power": $("#daily-power").val(),
            "rooms_available": $("#units_available").val(),
            "security_available": $("#security :selected").val(),
        };
        var payload = JSON.stringify(houseDict);
        return request.post('/houses', payload)
        .then((house) => {
            function img1() {
                // upload first image
                var formData = new FormData();
                var file = $("#Apart-image1");
                var ins = $("#Apart-image1")[0].files.length;
                if(ins == 0) {
                    return null;
                } else {
                    formData.append("file", file[0].files[0]);
                    formData.append("fileName", house.id + 'one');
                    formData.append("folder", "apartment-images");
            
                    return request.postFile(formData)
                }
            }

            function img2() {
                // Upload second image
                var formData2 = new FormData();
                var file = $("#Apart-image2")
                var ins = $("#Apart-image2")[0].files.length;
                if(ins == 0) {
                    return null;
                } else {
                    formData2.append("file", file[0].files[0]);
                    formData2.append("fileName", house.id + 'two');
                    formData2.append("folder", "apartment-images");

                    return request.postFile(formData2)
                }
            }

            function img3() {
                // Upload third image
                var formData3 = new FormData();
                var file = $("#Apart-image3");
                var ins = $("#Apart-image3")[0].files.length;
                if(ins == 0) {
                    return null;
                } else {
                    formData3.append("file", file[0].files[0]);
                    formData3.append("fileName", house.id + 'three');
                    formData3.append("folder", "apartment-images");
            
                    return request.postFile(formData3);
                }
            }

                // imgArray = [img1, img2, img3];
                // var removeNull = (val, idx, arr) => {
                //     if (val == null) {
                //         arr.splice(idx, 1);
                //         return true;
                //     } else {
                //         return false;
                //     }
                // }
                // imgArray.filter(removeNull);
            Promise.all([img1(), img2(), img3()])
            .then((values) => {
                var endpoint = '/houses/' + house.id;
                var values = values.filter((element) => element !== null);
                var load = {};
                var keys =['image1', 'image2', 'image3'];
                for (var i=0; i<values.length; i++) {
                    load[keys[i]] = values[i]
                }
                var payload = JSON.stringify(load)
                request.put(endpoint, payload)
                .then(() => {
                    showAlert("Images uploaded successfully", 'success');
                    getUserType();
                }).catch((err) => {
                    errorHandler(err, 'We encountered an error while uploading your images, please upload them again');
                })
            })
        }).catch((err) => {
            errorHandler(err, 'We encountered an error while uploading the apartment, please upload it again');
        })
    })
}

Promise.all([getEnvironment(), getStreet(), postApartment()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
}).catch((err) => {
    errorHandler(err, "failed to load page");
})