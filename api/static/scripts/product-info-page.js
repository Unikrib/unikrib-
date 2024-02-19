#!/usr/bin/node

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
const prodId = queryParams.get("id");
const userId = getWithExpiry("newId");

async function getProduct() {
    if (prodId != null) {
        const productInfo = await request.get('/products/' + prodId)
        return productInfo;
    } else {
        return null;
    }
}

// Load the product details
async function getProductDetail(productInfo) {
    var owner = await request.get('/users/' + productInfo.owner_id)
    var owner_com_res = await request.get('/environments/' + owner.com_res)
    for (var image of [productInfo.image1, productInfo.image2, productInfo.image3]) {
        if (image != null) {
            $('#product-images').append('<img src="' + image + '" alt="img" draggable="false">');
        }
    }
    loadImages()
    $('#prod-name').text(productInfo.name)
    $('#product-price').text('₦' + parsePrice(productInfo.price))
    $('#community').text(owner_com_res.name)
    if (productInfo.delivery === 'yes') {
        $('#delivery').removeClass('Unavailable')
        $('#delivery').addClass('Available')
        $('#delivery').text('Available')
    } else {
        $('#delivery').removeClass('Available')
        $('#delivery').addClass('Unavailable')
        $('#delivery').text('Unavailable')
    }
    $('#features').text(productInfo.features)
}

// Load the product owner details
async function getOwnerDetail(productInfo) {
    const owner = await request.get('/users/' + productInfo.owner_id)
    var owner_com_res = await request.get('/environments/' + owner.com_res);
    $('#profile-pic-cont').html('<img src="' + owner.avatar + '">')
    $('#name').html(`<p>` + owner.first_name + ` ` + owner.last_name + ` <icon class='fa fa-check-circle' id="verified"></icon></p>`)
    $('#community-select').text(owner_com_res.name);
    $('#uploader-phone').html('<p class="contact"><icon class="fa fa-phone"><a href="tel:' + owner.phone_no +'" class="contact-links"> Call</a></icon></p>')
    $('#uploader-whatsapp').html(`<p class="contact"><icon class="fa fa-whatsapp"><a href="https://api.whatsapp.com/send?phone=` + owner.phone_no + `"
        class="contact-links"> Whatsapp</a></icon></p>`)
    $("#rating").text(owner.rating.toFixed(1))
    if (!owner.isVerified) {
        $("#verified").addClass('disappear');
    }
}

// Load all the reviews for the owner
async function getReview(productInfo) {
    request.get('/users/' + productInfo.owner_id + '/reviews')
    .then((reviews) => {
        if (reviews.length === 0){
            $("#latest-review-cont").html('<p id="review-message"> No reviews have been left for this vendor yet.</p>');
            $("#other-reviews-cont").html(`
                <a href="review-page.html?id=` + productInfo.owner_id + `">
                <p id="">Add a new review</p>
                </a>`)
            var payload = JSON.stringify({
                "reviewee": productInfo.owner_id,
                "reviewer": userId
            })
            // return request.post('/review_eligibility', payload)
            // .then((res) => {
            //     if (res.message === 'false') {
            //         $("#other-reviews-cont").html('');
            //     } else if (res.message === 'true') {
            //         $("#other-reviews-cont").html(`
            //             <a href="review-page.html?id=` + productInfo.owner_id + `">
            //             <p id="">Add a new review</p>
            //             </a>`)
            //     }
            // })
        } else {
            $('#view-review').text('View all reviews')
            request.get('/users/' + reviews[0].reviewer)
            .then((reviewer) => {
                $("#latest-review-cont").html(`<div id="rev-img-cont">
                    <img src="` + reviewer.avatar + `">
                    </div>
                    <div id="rev-name-cont">
                        <p class="rev-name">` + reviewer.first_name + ` ` + reviewer.last_name + ` <icon class='fa fa-check-circle' id="verified-rev"></icon></p>
                    </div>
                    <div id="rev-message-cont">
                        <p id="review-message">` + reviews[0].text + `</p> 
                        <p class="time-stamp">` + reviews[0].updated_at.slice(0, 10) + `</p>
                    </div>`)
                if (reviews.length === 1){
                    var payload = JSON.stringify({
                        "reviewee": productInfo.owner_id,
                        "reviewer": userId
                    })
                    // return request.post('/review_eligibility', payload)
                    // .then((res) => {
                        $("#other-reviews-cont").html(`
                            <a href="review-page.html?id=` + productInfo.owner_id + `">
                            <p id="">Add a new review</p>
                            </a>`)
                    //     if (res.message === 'false') {
                    //         $("#other-reviews-cont").html('');
                    //     } else if (res.message === 'true') {
                    //         $("#other-reviews-cont").html(`
                    //             <a href="review-page.html?id=` + productInfo.owner_id + `">
                    //             <p id="">Add a new review</p>
                    //             </a>`)
                    //     }
                    // })
                } else {
                    $("#other-reviews-cont").html(`
                    <a href="review-page.html?id=` + productInfo.owner_id + `">
                    <p id="">Read all reviews</p>
                    </a>`)															
                }
                if (!reviewer.isVerified) {
                    $("#verified-rev").addClass('disappear');
                }
            })
        }
    }).catch((err) => {
        errorHandler(err, "Error loading owner ratings");
    })
}

function loadImages() {
    const carousel = document.querySelector(".carousel"),
    firstImg = carousel.querySelectorAll("img")[0],
    arrowIcons = document.querySelectorAll(".wrapper i");

    let isDragStart = false, isDragging = false, prevPageX, prevScrollLeft, positionDiff;

    const showHideIcons = () => {
        let scrollWidth = carousel.scrollWidth - carousel.clientWidth;
        arrowIcons[0].style.display = carousel.scrollLeft == 0 ? "none" : "block";
        arrowIcons[1].style.display = carousel.scrollLeft == scrollWidth ? "none" : "block";
    }

    arrowIcons.forEach(icon => {
        icon.addEventListener("click", () => {
            let firstImgWidth = firstImg.clientWidth + 14;
            carousel.scrollLeft += icon.id == "left" ? -firstImgWidth : firstImgWidth;
            setTimeout(() => showHideIcons(), 60);
        });
    });

    const autoSlide = () => {
        if(carousel.scrollLeft - (carousel.scrollWidth - carousel.clientWidth) > -1 || carousel.scrollLeft <= 0) return;

        positionDiff = Math.abs(positionDiff);
        let firstImgWidth = firstImg.clientWidth + 14;
        let valDifference = firstImgWidth - positionDiff;

        if(carousel.scrollLeft > prevScrollLeft) {
            return carousel.scrollLeft += positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
        }
        carousel.scrollLeft -= positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
    }

    const dragStart = (e) => {
        isDragStart = true;
        prevPageX = e.pageX || e.touches[0].pageX;
        prevScrollLeft = carousel.scrollLeft;
    }

    const dragging = (e) => {
        if(!isDragStart) return;
        e.preventDefault();
        isDragging = true;
        carousel.classList.add("dragging");
        positionDiff = (e.pageX || e.touches[0].pageX) - prevPageX;
        carousel.scrollLeft = prevScrollLeft - positionDiff;
        showHideIcons();
    }

    const dragStop = () => {
        isDragStart = false;
        carousel.classList.remove("dragging");

        if(!isDragging) return;
        isDragging = false;
        autoSlide();
    }

    carousel.addEventListener("mousedown", dragStart);
    carousel.addEventListener("touchstart", dragStart);

    document.addEventListener("mousemove", dragging);
    carousel.addEventListener("touchmove", dragging);

    document.addEventListener("mouseup", dragStop);
    carousel.addEventListener("touchend", dragStop);
}

Promise.all([getProduct()])
.then((productInfo) => {
    Promise.all([getProductDetail(productInfo[0]), getOwnerDetail(productInfo[0]), getReview(productInfo[0])])
    .then(() => {
        var loader = document.getElementById('preloader');
        if (loader != null) {
            loader.style.display = "none";
        }
    })
}).catch((err) => {
    errorHandler(err, "Failed to load page");
})
