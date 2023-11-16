#!/usr/bin/node
const houseId = getWithExpiry('houseId')

// Load the apartment details
async function getApartmentDetail() {
    return request.get('/houses/' + houseId)
    .then((house) => {
        if (house.apartment === 'Single-room') {
            $('#apartment').append('<option value="Single-room" selected>Single Room</option>')
        } else {
            $('#apartment').append('<option value="Single-room">Single Room</option>')
        }
        if (house.apartment === 'Self-contain') {
            $('#apartment').append('<option value="Self-contain" selected>Self-contain</option>')
        } else {
            $('#apartment').append('<option value="Self-contain">Self-contain</option>')
        }
        if (house.apartment === 'One-bedroom') {
            $('#apartment').append('<option value="One-bedroom" selected>One bedroom flat</option>')
        } else {
            $('#apartment').append('<option value="One-bedroom">One bedroom flat</option>')
        }
        if (house.apartment === 'Two-bedroom') {
            $('#apartment').append('<option value="Two-bedroom" selected>Two bedroom flat</option>')
        } else {
            $('#apartment').append('<option value="Two-bedroom">Two bedroom flat</option>')
        }
        if (house.apartment === 'Three-bedroom') {
            $('#apartment').append('<option value="Three-bedroom" selected>Three bedroom flat</option>')
        } else {
            $('#apartment').append('<option value="Three-bedroom">Three bedroom flat</option>')
        }
        if (house.newly_built) {
            $("#newly_built").append('<option value="True" selected>Yes</option>')
            $("#newly_built").append('<option value="False">No</option>')
        } else {
            $("#newly_built").append('<option value="True">Yes</option>')
            $("#newly_built").append('<option value="False" selected>No</option>')
        }
        if (house.security_available) {
            $("#security").append('<option value="True" selected>Yes</option>')
            $("#security").append('<option value="False">No</option>')
        } else {
            $("#security").append('<option value="True">Yes</option>')
            $("#security").append('<option value="False" selected>No</option>')
        }
        if (house.tiled) {
            $("#tiled").append('<option value="True" selected>Yes</option>')
            $("#tiled").append('<option value="False">No</option>')
        } else {
            $("#tiled").append('<option value="True">Yes</option>')
            $("#tiled").append('<option value="False" selected>No</option>')
        }
        if (house.agent_fee) {
            $("#agent-fee").text(house.agent_fee)
        }

        $('#name').val(house.name)
        $("#units_available").val(house.rooms_available)
        $("#daily-power").val(house.daily_power)
        var price = parseInt(house.price)
        $('#price').val(price)
        $("#apart-descript").val(house.features)
        $('#agent-fee').val(house.agent_fee)

        if (house.running_water === 'yes') {
            $('#running-water').append('<option value="yes" selected>Yes</option>')
        } else {
            $('#running-water').append('<option value="yes">Yes</option>')
        }
        if (house.running_water === 'no') {
            $('#running-water').append('<option value="no" selected>No</option>')
        } else {
            $('#running-water').append('<option value="no">No</option>')
        }

        if (house.waste_disposal === 'yes') {
            $('#Adequate-disposal').append('<option value="yes" selected>Yes</option>')
        } else {
            $('#Adequate-disposal').append('<option value="yes">Yes</option>')
        }
        if (house.waste_disposal === 'no') {
            $('#Adequate-disposal').append('<option value="no" selected>No</option>')
        } else {
            $('#Adequate-disposal').append('<option value="no">No</option>')
        }

        $('#Image1').html('<img id="image1" src="' + house.image1 + '">')
        $('#Image2').html('<img id="image2" src="' + house.image2 + '">')
        $('#Image3').html('<img id="image3" src="' + house.image3 + '">')
        request.get('/streets/' + house.street_id)
        .then((street) => {
            request.get('/environments/' + street.env_id)
            .then((env) => {
                request.get('/environments')
                .then((envs) => {
                    $.each(envs, function(_index, item){
                        if (item.name === env.name) {
                            $('#community').append('<option value="' + env.id + '" selected>' + env.name + '</option>')
                        } else {
                            $('#community').append('<option value="' + item.id + '">' + item.name + '</option>')
                        }
                    })
                    request.get('/environments/' + env.id + '/streets')
                    .then((strs) => {
                        $.each(strs, function (index, str){
                            if (str.name === street.name){
                                $('#street').append('<option value="' + street.id + '" selected>' + street.name + '</option>')
                            } else {
                                $("#street").append('<option value="' + str.id + '">' + str.name + '</option>')
                            }
                        })
                    })
                })
            })
        })
    }).catch((err) => {
        errorHandler(err, "Could not load the apartment details");
    })
}

// Load the corresponding streets when the community is changed
async function getStreet() {
    $('#community').on('change', function() {
        var env = $('#community :selected').val();
        return request.get('/environments/' + env + '/streets')
        .then((strs) => {
            $('#street').html('')
            $.each(strs, function(index, str){
                $('#street').append('<option value="' + str.id + '">' + str.name + '</option>')
            })
        }).catch((err => {
            errorHandler(err, "Could not load the streets in this environment")
        }))
    })
}

/* Image upload functions */
var img1 = () => {
    //update the new first image
    var formData = new FormData();
    var file = $("#Apart-image1");
    formData.append("file", file[0].files[0]);
    formData.append("fileName", houseId + 'one');
    formData.append("folder", "apartment-images");

    return request.postFile(formData)
}

var img2 = () => {
    //update the new second image
    var formData = new FormData();
    var file = $("#Apart-image2");
    formData.append("file", file[0].files[0]);
    formData.append("fileName", houseId + 'two');
    formData.append("folder", "apartment-images");

    return request.postFile(formData)
}

var img3 = () => {
    //update the new third image
    var formData = new FormData();
    var file = $("#Apart-image3");
    formData.append("file", file[0].files[0]);
    formData.append("fileName", houseId + 'three');
    formData.append("folder", "apartment-images");

    return request.postFile(formData)
}

// PUT the new data to the server
async function putDetail(){
    var image1 = false;
    var image2 = false;
    var image3 = false;
    
    $('#Apart-image1').on('change', function() {
        image1 = true;
    })
    $('#Apart-image2').on('change', function() {
        image2 = true;
    })
    $('#Apart-image3').on('change', function() {
        image3 = true;
    })
    $('#submit-apart').on('click', function(){
        var payload = JSON.stringify({
            "apartment": $('#apartment :selected').val(),
            "name": $('#name').val(),
            "street_id": $('#street :selected').val(),
            "price": $('#price').val(),
            "agent_fee": $("#agent-fee").val(),
            "running_water": $('#running-water :selected').val(),
            "waste_disposal": $('#Adequate-disposal :selected').val(), 
            "features": $("#apart-descript").val(),
            "newly_built": $("#newly_built :selected").val(),
            "tiled": $("#tiled :selected").val(),
            "rooms_available": $("#units_available").val(),
            "daily_power": $("#daily-power").val(),
            "security_available": $("#security :selected").val(),
        })
        var endpoint = '/houses/' + houseId;
        return request.put(endpoint, payload)
        .then(() => {
            if (image1 === false && image2 === false && image3 === false){
                window.location.href = 'apartment-info-page2.html?id=' + houseId
            } else {
                var imgArray = []
                if (image1 === true) {
                    imgArray.push(img1())
                }
                if (image2 === true) {
                    imgArray.push(img2())
                }
                if (image3 === true) {
                    imgArray.push(img3())
                }
                Promise.all(imgArray).then((values) => {
                    load = {}
                    if (image1 === true) {
                        load["image1"] = values.shift();
                    }
                    if (image2 === true) {
                        load["image2"] = values.shift();
                    }
                    if (image3 === true) {
                        load["image3"] = values.shift()
                    }
                    var payload = JSON.stringify(load);
                    var endpoint = '/houses/' + houseId;
                    request.put(endpoint, payload)
                    .then(() => {
                        window.location.href = 'apartment-info-page2.html?id=' + houseId;
                    }).catch((err) => {
                        errorHandler(err, 'Could not update images, please try again');
                    })
                })
            }
        }).catch((err) => {
            errorHandler(err, "Could not update apartment, please try again");
        })
    })
}

Promise.all([getApartmentDetail(), getStreet(), putDetail()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
}).catch((err) => {
    errorHandler(err, "failed to load page");
})