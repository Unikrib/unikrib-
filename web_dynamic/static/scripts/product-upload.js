#!/usr/bin/node

const userId = getWithExpiry('newId')
// Load the available categories
async function getCategories(){
    return request.get('/categories')
    .then((cats) => {
        $.each(cats, function (index, cat) {
            $('#product-category').append('<option value="' + cat.id + '">' + cat.name + '</option>')
        })
    }).catch((err) => {
        errorHandler(err, "Could not load available categories");
    })
}

// Post new product
async function postProduct(){
    $('#submit-product').on('click', function(){
        payload = JSON.stringify({
            "name": $('#product-name').val(),
            "price": $('#price').val(),
            "features": $("#product-features").val(),
            "delivery": $('#delivery-status :selected').val(),
            "category_id": $('#product-category :selected').val(),
            "owner_id": userId,
            "available": $('#product-status :selected').val(),
        });

        return request.post('/products', payload)
        .then((product) => {
            var img1 = () => {
                // upload first image
                var formData1 = new FormData();
                var file = $("#product-image1");
                var ins = $("#product-image1")[0].files.length;
                if(ins == 0) {
                    return null;
                } else {
    
                formData1.append("file", file[0].files[0]);
                formData1.append("fileName", product.id + 'one');
                formData1.append("folder", "productImages");
    
                return request.postFile(formData1)
                }
            }
    
            var img2 = () => {
                // Upload second image
                var formData2 = new FormData();
                var file = $("#product-image2");
                var ins = $("#product-image2")[0].files.length;
                if (ins == 0) {
                    return null;
                } else {
                    formData2.append("file", file[0].files[0]);
                    formData2.append("fileName", product.id + 'two');
                    formData2.append("folder", "productImages");
    
                    return request.postFile(formData2)
                }
            }
    
            var img3 = () => {
                // Upload third image
                var formData3 = new FormData();
                var file = $("#product-image3");
                var ins = $("#product-image3")[0].files.length;
                if(ins == 0) {
                    return null;
                } else {
                    formData3.append("file", file[0].files[0]);
                    formData3.append("fileName", product.id + 'three');
                    formData3.append("folder", "productImages");
    
                    return request.postFile(formData3)
                }
            }
    
            imgArray = [img1(), img2(), img3()]
            var imgArray = imgArray.filter((element) => element !== null);
            Promise.all(imgArray).then((values) => {
                var endpoint = '/products/' + product.id;
                var load = {}
                if (values[0]) {
                    load['image1'] = values[0];
                }
                if (values[1]) {
                    load['image2'] = values[1];
                }
                if (values[2]) {
                    load['image3'] = values[2];
                }
                load = JSON.stringify(load)
                request.put(endpoint, load)
                .then(() => {
                    showAlert("Product uploaded successfully", 'success');
                    getUserType();
                }).catch((err) => {
                    errorHandler(err, "We were unable to upload your product images, please try again");
                })
            })
        }).catch((err) => {
            errorHandler(err, "We were unable to upload product, please try again");
        })
    })
}

Promise.all([getCategories(), postProduct()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Fail to load page");
})