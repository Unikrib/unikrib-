#!/usr/bin/env python3
const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
const serviceId = queryParams.get("id");
const userId = getWithExpiry("newId");

async function getServices() {
    if (serviceId != null){
        const service = await request.get('/services/' + serviceId)
        return service;
    } else {
        return null;
    }
}

// Load service images
async function getImages(serviceInfo){
    serviceImages = [serviceInfo.image1, serviceInfo.image2, serviceInfo.image3, serviceInfo.image4, serviceInfo.image5]
    for (var i=1; i<=5; i++){
        $('#images').append(`<img src="` + serviceImages[i-1] + `" alt="img" draggable="false">`)
    }
    loadImages()
}

// Load owner details
async function getOwnerDetails(serviceInfo){
    const owner = await request.get('/users/' + serviceInfo.owner_id)
    const owner_com_res = await request.get('/environments/' + owner.com_res)
    const category = await request.get('/service-categories/' + serviceInfo.category_id)
    $('#profile-cont').append(`<div id="profile-pic-cont">
        <img src="` + owner.avatar + `">
        </div>
        <div id="name-cont">
            <p class="name">` + owner.first_name + ` ` + owner.last_name + ` <icon class='fa fa-check-circle' id="verified"></icon></p>
            <p class="services" id="service-select">` + category.name + `</span></p>
            <p class="community" id="community-select">` + owner_com_res.name + `</p>
            <p class="rating">Average rating: <span id="">` + owner.rating.toFixed(1) + `</span><icon class="fa fa-star"></icon></span></p>
            <p class="bio">` + serviceInfo.description + `</p>
        </div>
        <div id="contact-cont">
            <div id="uploader-phone">
                <p class="contact"><icon class="fa fa-phone"><a href="tel:` + owner.phone_no + `" class="contact-links"> Call</a></icon></p>
            </div>
            <div id="uploader-whatsapp">
                <p class="contact"><icon class="fa fa-whatsapp"><a href="https://api.whatsapp.com/send?phone=` + owner.phone_no + `"
                    class="contact-links"> Whatsapp</a></icon></p>
            </div>
        </div>`)
    if (!owner.isVerified) {
        $("#verified").addClass("disappear");
    }
}

// Load reviews
async function getReviews(serviceInfo){
    request.get('/users/' + serviceInfo.owner_id + '/reviews')
    .then((reviews) => {
        $("#other-reviews-cont").on('click', function() {
            window.location.href = 'review-page.html';
        })
        $('#other-reviews-cont').html(`<a href="review-page.html">
                                        <p id="view-review"></p>`)
        if (reviews.length === 0){
            $("#latest-review-cont").html('<p id="review-message"> No review has been left for this user yet.</p>');
            $("#other-reviews-cont").html(`
                <a href="review-page.html?id=` + serviceInfo.owner_id + `">
                <p id="">Add a new review</p>
                </a>`)
            // var payload = JSON.stringify({
            //     "reviewee": productInfo.owner_id,
            //     "reviewer": userId
            // })
            // return request.post('/review_eligibility', payload)
            // .then((res) => {
            //     if (res.message === 'false') {
            //         $("#other-reviews-cont").html('');
            //     } else if (res.message === 'true') {
            //         $("#other-reviews-cont").html(`
            //             <a href="review-page.html?id=` + serviceInfo.owner_id + `">
            //             <p id="">Add a new review</p>
            //             </a>`)
            //     }
            // })
        } else {
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
                    $("#other-reviews-cont").html(`
                        <a href="review-page.html?id=` + serviceInfo.owner_id + `">
                        <p id="">Add a new review</p>
                        </a>`)
                    // var payload = JSON.stringify({
                    //     "reviewee": productInfo.owner_id,
                    //     "reviewer": userId
                    // })
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
                    $("#other-reviews-cont").html(`
                    <a href="review-page.html?id=` + serviceInfo.owner_id + `">
                    <p id="">Read all reviews</p>
                    </a>`)
                }
                if (!reviewer.isVerified) {
                    $("#verified-rev").addClass("disappear");
                }
            })
        }
    }).catch((err) => {
        errorHandler(err, "Could not load owner reviews");;
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

Promise.all([getServices()])
.then((service) => {
    Promise.all([getImages(service[0]), getOwnerDetails(service[0]), getReviews(service[0])])
    .then(() => {
        var loader = document.getElementById('preloader');
        if (loader != null) {
            loader.style.display = "none";
        }
    })
}).catch((err) => {
    errorHandler(err, "Error loading page")
})

