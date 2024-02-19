#!/usr/bin/node

const serviceId = getWithExpiry('serviceId')

// load the existing service images
$(function() {
    request.get('/services/' + serviceId)
    .then((service) => {
        $('#Image1').html('<img id="image1" src="' + service.image1 + '">')
        $('#Image2').html('<img id="image2" src="' + service.image2 + '">')
        $('#Image3').html('<img id="image3" src="' + service.image3 + '">')
        $('#Image4').html('<img id="image4" src="' + service.image4 + '">')
        $('#Image5').html('<img id="image5" src="' + service.image5 + '">')
    })
})
var image1 = false
var image2 = false
var image3 = false
var image4 = false
var image5 = false

$("#service-image1").on('change', function(){
    image1 = true
})
$('#service-image2').on('change', function() {
    image2 = true
})
$('#service-image3').on('change', function() {
    image3 = true
})
$('#service-image4').on('change', function() {
    image4 = true
})
$('#service-image5').on('change', function() {
    image5 = true
})
$(function() {
    $('#imgs-submit').on('click', function() {
        // Upload first image if changed
        var img1 = () => {
            if (image1 === true) {
                var formData = new FormData();
                var file = $("#service-image1");
                var ins = $("#service-image1")[0].files.length;
                if(ins == 0) {
                    showAlert("First image cannot be empty", 'warning')
                    return;
                }

                formData.append("file", file[0].files[0]);
                formData.append("fileName", serviceId + 'one');
                formData.append("folder", "serviceImages");

                return request.postFile(formData);
            } else {
                return null;
            }
        };

        // Upload second image if changed
        var img2 = () => {
            if (image2 === true) {
                var formData = new FormData();
                var file = $("#service-image2");
                var ins = $("#service-image2")[0].files.length;
                if(ins == 0) {
                    return;
                }
        
                formData.append("file", file[0].files[0]);
                formData.append("fileName", serviceId + 'two');
                formData.append("folder", "serviceImages");

                return request.postFile(formData)
            } else {
                return null;
            }
        };

        // Upload third image if changed
        var img3 = () => {
            if (image3 === true) {
                var formData = new FormData();
                var file = $("#service-image3");
                var ins = $("#service-image3")[0].files.length;
                if(ins == 0) {
                    return;
                }
        
                formData.append("file", file[0].files[0]);
                formData.append("fileName", serviceId + 'three');
                formData.append("folder", "serviceImages");

                return request.postFile(formData)
            } else {
                return null;
            }
        };

        // Upload fourth image if changed
        var img4 = () => {
            if (image4 === true) {
                var formData = new FormData();
                var file = $("#service-image4");
                var ins = $("#service-image4")[0].files.length;
                if(ins == 0) {
                    return;
                }
        
                formData.append("file", file[0].files[0]);
                formData.append("fileName", serviceId + 'four');
                formData.append("folder", "serviceImages");

                return request.postFile(formData)
            } else {
                return null;
            }
        };

        // Upload fifth image if changed
        var img5 = () => {
            if (image5 === true) {
                var formData = new FormData();
                var file = $("#service-image5");
                var ins = $("#service-image5")[0].files.length;
                if(ins == 0) {
                    return;
                }
        
                formData.append("file", file[0].files[0]);
                formData.append("fileName", serviceId + 'five');
                formData.append("folder", "serviceImages");

                return request.postFile(formData)
            } else {
                return null;
            }
        };

        var imgArray = [img1(), img2(), img3(), img4(), img5()]
        var imgArray = imgArray.filter((element) => element !== null);

        Promise.all(imgArray).then((values) => {
            var load = {};
            if (image1 === true) {
                load["image1"] = values.shift();
            }
            if (image2 === true) {
                load["image2"] = values.shift();
            }
            if (image3 === true) {
                load["image3"] = values.shift();
            }
            if (image4 === true) {
                load["image4"] = values.shift();
            }
            if (image5 === true) {
                load["image5"] = values[0];
            }
            var payload = JSON.stringify(load);
            var endpoint = '/services/' + serviceId;
            request.put(endpoint, payload)
            .then(() => {
                showAlert("Images uploaded sucessfully", 'success');
                getUserType();
            }).catch((err) => {
                errorHandler(err, 'We encountered an error while uploading your images, please try again later')
            })
        }).catch((err) => {
            errorHandler(err, 'We encountered an error while uploading your images, please try again later')
        })
    })
})
var loader = document.getElementById('preloader');
if (loader != null) {
    loader.style.display = "none";
}