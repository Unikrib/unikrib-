#!/usr/bin/node

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
const productId = queryParams.get("id");

// const productId = getWithExpiry('productId');
const userId = getWithExpiry('newId');

// Load product images
async function getProductImages(product){
	$("#apartment-slide-cont").html('')
	var count = 0;
	if (product.image1 != null){
		count += 1
	}
	if (product.image2 != null){
		count += 1
	}
	if (product.image3 != null){
		count += 1;
	}

	for (let i = 1; i <= count; i++){
		var image;
		if (i === 1){
			image = product.image1;
		} else if (i === 2) {
			image = product.image2;
		} else if (i === 3){
			image = product.image3;
		}
		$("#carousel").append('<img src="' + image + '" alt="img" draggable="false">')
		loadProduct()
	}
}
function loadProduct() {
	const carousel = document.querySelector(".carousel"),
	firstImg = carousel.querySelectorAll("img")[0],
	arrowIcons = document.querySelectorAll(".wrapper i");
	let isDragStart = false, isDragging = false, prevPageX, prevScrollLeft, positionDiff;
	const showHideIcons = () => {
		// showing and hiding prev/next icon according to carousel scroll left value
		let scrollWidth = carousel.scrollWidth - carousel.clientWidth; // getting max scrollable width
		arrowIcons[0].style.display = carousel.scrollLeft == 0 ? "none" : "block";
		arrowIcons[1].style.display = carousel.scrollLeft == scrollWidth ? "none" : "block";
	}
	arrowIcons.forEach(icon => {
		icon.addEventListener("click", () => {
			let firstImgWidth = firstImg.clientWidth + 14; // getting first img width & adding 14 margin value
			// if clicked icon is left, reduce width value from the carousel scroll left else add to it
			carousel.scrollLeft += icon.id == "left" ? -firstImgWidth : firstImgWidth;
			setTimeout(() => showHideIcons(), 60); // calling showHideIcons after 60ms
		});
		});
	const autoSlide = () => {
	// if there is no image left to scroll then return from here
	if(carousel.scrollLeft - (carousel.scrollWidth - carousel.clientWidth) > -1 || carousel.scrollLeft <= 0) return;
		positionDiff = Math.abs(positionDiff); // making positionDiff value to positive
		let firstImgWidth = firstImg.clientWidth + 14;
		// getting difference value that needs to add or reduce from carousel left to take middle img center
		let valDifference = firstImgWidth - positionDiff;
		if(carousel.scrollLeft > prevScrollLeft) { // if user is scrolling to the right
		return carousel.scrollLeft += positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
	}
	// if user is scrolling to the left
	carousel.scrollLeft -= positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
	}
	const dragStart = (e) => {
	// updatating global variables value on mouse down event
	isDragStart = true;
	prevPageX = e.pageX || e.touches[0].pageX;
	prevScrollLeft = carousel.scrollLeft;
	}
	const dragging = (e) => {
	// scrolling images/carousel to left according to mouse pointer
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

// Load product info
async function getProductInfo(product){
	if (product.delivery === 'yes'){
		var status = "Available";
	} else {
		var status = "Unavailable";
	}
	$('#product-details').html(`
		<p class="product-results"><span class="product-name">` + product.name + ` </span></p>
		<p class="price-results"><span class="product-price" id="product-price-1">N` + parsePrice(product.price) + `</span></p>
		<p class="delivery">Delivery: <span class="Available" id="delivery">` + status + `</span></p>`)
	if (product.delivery === 'yes'){
		$('#delivery').removeClass('Unavailable')
		$('#delivery').addClass('Available')
	} else {
		$('#delivery').addClass('Unavailable')
		$('#delivery').removeClass('Available')
	}
	$('#features').text(product.features)
}

// Load owner details
async function getOwnerInfo(){
	return request.get('/user/profile')
	.then((owner) => {
		request.get('/environments/' + owner.com_res)
		.then((env) => {
			$('#profile-cont').html(`
				<div id="profile-pic-cont">
					<img src="` + owner.avatar + `">
				</div>
				<div id="name-cont">
					<p class="name">`+ owner.first_name + ` ` + owner.last_name + ` <icon class='fa fa-check-circle' id="verified"></icon></p>
					<p class="services" id="service-select">Vendor</span></p>
					<p class="community" id="community-select">` + env.name + `</p>
					<p class="rating">Average rating: <span id="">` + owner.rating.toFixed(1) + `</span><icon class="fa fa-star"></icon></span></p>
					<p class="bio">` + owner.note + `</p>
				</div>`)
			if (!owner.isVerified) {
				$("#verified").addClass("disappear")
			}
		})
	})
}

// Load reviewers details
async function getReview(owner){
    setWithExpiry('revieweeId', userId);
	return request.get('/users/' + owner.id + '/reviews')
	.then((reviews) => {
		if (reviews.length === 0){
			$("#latest-review-cont").html('<p id="review-message"> No reviews have been left for you yet.</p>');
			$("#view-review").text("Add a new review")
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
				if (reviews.length === 1) {
					$("#view-review").text("Add a new review")
				} else {
					$("#view-review").text("View all reviews")
				}
				if (!reviewer.isVerified) {
					$("#verified-rev").addClass('disappear');
				}
			})
		}
	}).catch((err) => {
		errorHandler(err, "Could not load reviewer details");
	})
}

request.get('/products/' + productId)
.then((product) => {
	Promise.all([getProductImages(product), getProductInfo(product), getOwnerInfo(), getReview(product.owner_id)])
	.then(() => {
		var loader = document.getElementById('preloader');
		if (loader != null) {
			loader.style.display = "none";
		}
	})
	.catch((err) => {
		errorHandler(err, "Failed to load page");
	})
})
