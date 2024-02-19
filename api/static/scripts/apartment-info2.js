#!/usr/bin/node

// const houseId = getWithExpiry('houseId');
const userId = getWithExpiry('newId');

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
const houseId = queryParams.get("id");


async function getHouse() {
	if (houseId != null) {
		const house = await request.get("/houses/" + houseId);
		return house
	} else {
		showAlert("Apartment not found");
		return null
	}
}

// Load the apartment images
async function getImages(house) {
	$("#apartment-slide-cont").html('')
	for (let i = 1; i <= 3; i++){
		var image;
		if (i === 1){
			image = house.image1;
		} else if (i === 2) {
			image = house.image2;
		} else if (i === 3){
			image = house.image3;
		}
		$("#carousel").append('<img src="' + image + '" alt="img" draggable="false">')
	}
	loadImages()
}
function loadImages() {
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

// Load apartment info
async function getInfo(house) {
	const street = await request.get('/streets/' + house.street_id)
	const env = await request.get('/environments/' + street.env_id)
	$("#apartment-details").html(`<p class="address-results"><span class="type">`
		+ house.apartment + `</span> in <span class="hostel" id="hostel1">` + house.name
		+ ` </span>for rent <span class ="street" id="street1">` + street.name
		+ ` street,</span><span class ="community" id="community1"> ` + env.name + ` </span></p>
		<p class="price-results"><span class="price" id="price1">N` + parsePrice(house.price)
		+ ` </span>per year</p>`)
	if (house.running_water === 'yes'){
		$('#feature-cont').append('<p class="feature"><icon class="fa fa-tint"></icon> Running water available</p>');
	}
	if (house.waste_disposal === 'yes'){
		$('#feature-cont').append('<p class="feature"><icon class="fa fa-trash"></icon> waste disposal available</p>');
	}
	$("#feature-cont").append('<p>' + house.features + '</p>')
}

// Load owner details
async function getOwnerDetail(house) {
	const user = await request.get('/users/' + house.owner_id)
	if (user.avatar === null){
		var src1 = "images/photo5.png"
	} else {
		var src1 = user.avatar
	}
	$("#profile-cont").html(`<div id="profile-pic-cont">
			<img src="` + src1 + `">
		</div>
		<div id="name-cont">
			<p class="name"><span id="fname">` + user.first_name + ` </span><span id="lname"> ` + user.last_name + `</span>  <icon class='fa fa-check-circle' id="verified"></icon></p>
			<p class="services" id="service-select">Agent</span></p>
			<p class="community2" id="community-select">Ekosodin</p>
			<p class="rating">Average rating: <span id="">` + user.rating.toFixed(1) + `</span><icon class="fa fa-star"></icon></span></p>
			<p class="bio">` + user.note + `</p>
		</div>`);
	if (!user.isVerified) {
		$("#verified").addClass('disappear');
	}
}

// Load reviews
async function getReview(house) {
	setWithExpiry('revieweeId', house.owner_id);
	const reviews = await request.get('/users/' + house.owner_id + '/reviews')
	if (reviews.length === 0){
		$("#latest-review-cont").html('<p id="review-message"> No reviews have been left for you yet.</p>');
	} else {
		request.get('/users/' + reviews[0].reviewer)
		.then((reviewer) => {
			$("#latest-review-cont").html(`<div id="rev-img-cont">
				<img src="` + reviewer.avatar + `">
				</div>
				<div id="rev-name-cont">
					<p class="rev-name">` + reviewer.first_name + ` ` + reviewer.last_name + `  <icon class='fa fa-check-circle' id="verified-rev"></icon></p>
				</div>
				<div id="rev-message-cont">
					<p id="review-message">` + reviews[0].text + `</p> 
					<p class="time-stamp">` + reviews[0].updated_at.slice(0, 10) + `</p>
				</div>`)
			if (!reviewer.isVerified) {
				$("#verified-rev").addClass('disappear');
			}
		})
	}
}

Promise.all([getHouse()])
.then((house) => {
	Promise.all([getImages(house[0]), getInfo(house[0]), getOwnerDetail(house[0]), getReview(house[0])])
	.then(() => {
		var loader = document.getElementById('preloader');
		if (loader != null) {
			loader.style.display = "none";
		}
	})
})
.catch((err) => {
	errorHandler(err, "Failed to load page");
})