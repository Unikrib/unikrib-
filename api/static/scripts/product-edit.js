#!/usr/bin/node
const productId = getWithExpiry('productId');

// Load the product details
async function getProductInfo() {
    return request.get('/products/' + productId)
    .then((product) => {
        $('#Image1').html('<img id="image1" src="' + product.image1 + '">')
        $('#Image2').html('<img id="image2" src="' + product.image2 + '">')
        $('#Image3').html('<img id="image3" src="' + product.image3 + '">')

        request.get('/categories')
        .then((cats) => {
            $.each(cats, function(index, cat) {
                if (cat.id === product.category_id){
                    $('#product-category').append('<option value="' + cat.id + '" selected>' + cat.name + '</option>');
                } else {
                    $('#product-category').append('<option value="' + cat.id + '">' + cat.name + '</option>');
                }
            })
        }).catch((err) => {
            errorHandler(err, "Could not load product categories")
        })
        $('#product-name').val(product.name);
        $('#price').val(product.price);
        $('#product-features').val(product.features);
        if (product.delivery === 'yes') {
            $('#delivery-status').append('<option value="yes" selected>Available</option>')
        } else {
            $('#delivery-status').append('<option value="yes">Available</option>');
        }
        if (product.delivery === 'no') {
            $('#delivery-status').append('<option value="no" selected>Unavailable</option>')
        } else {
            $('#delivery-status').append('<option value="no">Unavailable</option>');
        }
        if (product.available === 'no'){
            $('#product-status').append('<option value="yes">In stock</option>')
            $('#product-status').append('<option value="no" selected>Out of stock</option>')
        } else {
            $('#product-status').append('<option value="yes" selected>In stock</option>')
            $('#product-status').append('<option value="no">Out of stock</option>')
        }
    })
}

/**  Define the image upload functions*/   
// Upload first image
var img1 = () => {
    var formData = new FormData();
    var file = $("#product-image1");
    formData.append("file", file[0].files[0]);
    formData.append("fileName", productId + 'one');
    formData.append("folder", "productImages");

    return request.postFile(formData)
}

// Upload second image
var img2 = () => {
    var formData = new FormData();
    var file = $("#product-image2");
    formData.append("file", file[0].files[0]);
    formData.append("fileName", productId + 'two');
    formData.append("folder", "productImages");

    return request.postFile(formData)
}

// Upload third image
var img3 = () => {
    var formData = new FormData();
    var file = $("#product-image3");
    formData.append("file", file[0].files[0]);
    formData.append("fileName", productId + 'three');
    formData.append("folder", "productImages");

    return request.postFile(formData)
}

// PUT the updated product to storage
async function putNewInfo() {
    var image1 = false;
    var image2 = false;
    var image3 = false;
    
    $('#product-image1').on('change', function() {
        image1 = true;
    })
    $('#product-image2').on('change', function() {
        image2 = true;
    })
    $('#product-image3').on('change', function() {
        image3 = true;
    })
    $('#Submit-product').on('click', function(){
        imgArray = []
        if (image1 === true) {
            imgArray.push(img1());
        }
        if (image2 === true) {
            imgArray.push(img2());
        }
        if (image3 === true) {
            imgArray.push(img3())
        }
        Promise.all(imgArray).then((values) => {
            var payload = {
                "category_id": $('#product-category :selected').val(),
                "name": $('#product-name').val(),
                "price": $('#price').val(),
                "features": $('#product-features').val(),
                "delivery": $('#delivery-status :selected').val(),
                "available": $('#product-status :selected').val(),
            }
            if (image1 === true) {
                payload["image1"] = values.shift();
            }
            if (image2 === true) {
                payload["image2"] = values.shift();
            }
            if (image3 === true) {
                payload["image3"] = values.shift();
            }
            var endpoint = '/products/' + productId;
            var payload = JSON.stringify(payload)
            request.put(endpoint, payload)
            .then(() => {
                showAlert("Details uploaded successfully", 'success');
                getUserType();
            }).catch((err) => {
                errorHandler(err, "Error!, please refresh the page and try again");
            })
        })
    })
}

Promise.all([getProductInfo(), putNewInfo()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Failed to load page");
})