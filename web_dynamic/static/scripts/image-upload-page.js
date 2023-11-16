#!/usr/bin/node

const userId = getWithExpiry('newId');
const serviceId = getWithExpiry('serviceId')

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

$(function (){
    $('#imgs-submit').on('click', function (){
        // Upload first image
        var img1 = () => {
            var formData = new FormData();
            var file = $("#service-image1");
            var ins = $("#service-image1")[0].files.length;
            if(ins == 0) {
                return null;
            } else {
                formData.append("file", file[0].files[0]);
                formData.append("fileName", serviceId + 'one');
                formData.append("folder", "serviceImages");

                return request.postFile(formData)
            }
        }

        // Upload second image
        var img2 = () => {
            var formData2 = new FormData();
            var file = $("#service-image2");
            var ins = $("#service-image2")[0].files.length;
            if(ins == 0) {
                return null;
            } else {
                formData2.append("file", file[0].files[0]);
                formData2.append("fileName", serviceId + 'two');
                formData2.append("folder", "serviceImages");

                return request.postFile(formData2);
            }
        }

        // Upload third image
        var img3 = () => {
            var formData3 = new FormData();
            var file = $("#service-image3");
            var ins = $("#service-image3")[0].files.length;
            if(ins == 0) {
                return null;
            } else {
                formData3.append("file", file[0].files[0]);
                formData3.append("fileName", serviceId + 'three');
                formData3.append("folder", "serviceImages");

                return request.postFile(formData3)
            }
        }

        // upload fourth image
        var img4 = () => {
            var formData4 = new FormData();
            var file = $("#service-image4");
            var ins = $("#service-image4")[0].files.length;
            if(ins == 0) {
                return null;
            } else {
                formData4.append("file", file[0].files[0]);
                formData4.append("fileName", serviceId + 'four');
                formData4.append("folder", "serviceImages");

                return request.postFile(formData4)
            }
        }

        // Upload fifth image
        var img5 = () => {
            var formData5 = new FormData();
            var file = $("#service-image5");
            var ins = $("#service-image5")[0].files.length;
            if(ins == 0) {
                return null;
            } else {
                formData5.append("file", file[0].files[0]);
                formData5.append("fileName", serviceId + 'five');
                formData5.append("folder", "serviceImages");

                return request.postFile(formData5);
            }
        }

        imgArray = [img1(), img2(), img3(), img4(), img5()];
        var imgArray = imgArray.filter((element) => element !== null);

        Promise.all(imgArray).then((values) => {
            var endpoint = '/services/' + serviceId;
            var load = {};
            var images = {"image1": image1, "image2": image2, "image3": image3,
                            "image4": image4, "image5": image5}
            for (var image in images) {
                if (images[image] === true) {
                    load[image] = values.shift()
                }
            }
            var payload = JSON.stringify(load)
            request.put(endpoint, payload)
            .then(() => {
                showAlert("Images uploaded successfully", 'success');
                window.location.href = 'signup-confirmpage.html'
            }).catch((err) => {
                errorHandler(err, 'We encountered an error while uploading your images, please upload them again');
            })
        })
    })
})
var loader = document.getElementById('preloader');
if (loader != null) {
    loader.style.display = "none";
}