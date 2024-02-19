#!/usr/bin/node

// const houseInfo = getDict('itemInfo');
const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
const houseId = queryParams.get("id");

const userId = getWithExpiry('newId')

async function getHouseInfo() {
	if (houseId != null) {
		try {
			var houseInfo = await request.get('/houses/' + houseId)
			return houseInfo;
		} catch (err) {
			if (err.status === 404) {
				Swal.fire({
					icon: 'error',
					title: 'Oops...',
					text: 'The apartment you are requesting is invalid or has been removed',
					footer: '<a href="Apartment-page.html">View other apartments</a>'
				  })
			} else {
				errorHandler(err, "Failed to load page, please reload")
			}
			return null;
		}
	} else {
		showAlert("Apartment not found", "error");
		return null
	}
}

// Load apartment images
async function getImages(houseInfo) {
	$("#apartment-slide-cont").html('')
				
	for (let i = 1; i <= 3; i++){
		var image;
		if (i === 1){
			image = houseInfo.image1;
		} else if (i === 2) {
			image = houseInfo.image2;
		} else if (i === 3){
			image = houseInfo.image3;
		}
		$("#apart-images").append(`<img src="` + image + `" alt="img" draggable="false">`)
		loadImages()
	}
}

// Load house info
async function getApartmentInfo(houseInfo) {
	const street = await request.get('/streets/' + houseInfo.street_id)
	const env = await request.get('/environments/' + street.env_id)
	$("#apartment-details").html(` <p class="address-results"><span class="type">`
		+ houseInfo.apartment + `</span> in <span class="hostel" id="hostel1">` + houseInfo.name
		+ ` </span>for rent <span class ="street" id="street1">` + street.name
		+ ` street,</span><span class ="community" id="community1"> ` + env.name + ` </span></p>
		<p class="price-results"><span class="price" id="price1">₦` + parsePrice(houseInfo.price)
		+ ` </span>per year</p>`)
	if (houseInfo.running_water === 'yes'){
		$('#feature-cont').append('<p class="feature"><icon class="fa fa-tint"></icon> Running waters available</p>');
	}
	if (houseInfo.waste_disposal === 'yes'){
		$('#feature-cont').append('<p class="feature"><icon class="fa fa-trash"></icon> waste disposal available</p>');
	}
	if (houseInfo.agent_fee && houseInfo.agent_fee > 0) {
		$("#feature-cont").append('<p class="feature"> Agent fee: ₦' + houseInfo.agent_fee + '</p>')
	} if (houseInfo.tiled === true) {
		$("#feature-cont").append('<p class="feature"> Tiled</p>')
	} 
	$("#feature-cont").append("<p>" + houseInfo.features + "<p>");
}

// Load owner details
async function getOwnerDetail(houseInfo) {
	$("#report-cont").html(`
		<a href="report.html?reported=` + houseInfo.owner_id + `">
		<div id="report-button"><icon class="fa fa-flag"></icon> Report</div>
  		</a>`)
	return request.get('/users/' + houseInfo.owner_id)
	.then((user) => {
		$("#profile-cont").html(`<div id="profile-pic-cont">
				<img src="` + user.avatar + `">
			</div>
			<div id="name-cont">
				<p class="name"><span id="fname">` + user.first_name + ` </span><span id="lname"> ` + user.last_name + `</span>` + ` <icon class='fa fa-check-circle' id="verified"></icon></p>
				<p class="services" id="service-select">Agent</span></p>
				<p class="community2" id="community-select">Ekosodin</p>
				<p class="rating"><span id=""> ` + user.rating.toFixed(1) + `</span><icon class="fa fa-star"></icon></span></p>
				<p class="bio">` + user.note + `</p>
			</div>`);
		$("#uploader-phone").html(`<p class="contact"><icon class="fa fa-phone">
				<a href="tel:` + user.phone_no + `" class="contact-links"> Call</a></icon></p>`)
		$("#uploader-whatsapp").html(`<p class="contact"><icon class="fa fa-whatsapp">
			<a href="https://api.whatsapp.com/send?phone=` + user.phone_no + `" class="contact-links"> Whatsapp</a></icon></p>`)
		if (!user.isVerified) {
			$("#verified").addClass('disappear');
		}
	})
}

// Load reviews
async function getReviews(houseInfo) {
	// setWithExpiry('revieweeId', houseInfo.owner_id);
	return request.get('/users/' + houseInfo.owner_id + '/reviews')
	.then((reviews) => {
		if (reviews.length === 0){
			$("#latest-review-cont").html('<p id="review-message"> No reviews have been left for this agent yet.</p>');

			var payload = JSON.stringify({
				"reviewee": houseInfo.owner_id,
				"reviewer": userId
			})
			return request.post('/review_eligibility', payload)
			.then((res) => {
				if (res.message === 'false') {
					$("#other-reviews-cont").html('');
				} else if (res.message === 'true') {
					$("#other-reviews-cont").html(`
						<a href="review-page.html?id=` + houseInfo.owner_id + `">
						<p id="">Add a new review</p>
						</a>`)
				}
			})
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
				if (reviews.length === 1){
					var payload = JSON.stringify({
						"reviewee": houseInfo.owner_id,
						"reviewer": userId
					})
					return request.post('/review_eligibility', payload)
					.then((res) => {
						if (res.message === 'false') {
							$("#other-reviews-cont").html('');
						} else if (res.message === 'true') {
							$("#other-reviews-cont").html(`
								<a href="review-page.html?id=` + houseInfo.owner_id + `">
								<p id="">Add a new review</p>
								</a>`)
						}
					})
				} else {
					$("#other-reviews-cont").html(`
						<a href="review-page.html?id=` + houseInfo.owner_id + `">
						<p id="">Read all reviews</p>
			  			</a>`)
				}
				if (!reviewer.isVerified) {
					$("#verified-rev").addClass('disappear');
				}
			})
		}
	})
}

// contact agent button handler
async function contactAgent(houseInfo) {
	$("#confirm-vac-cont").on('click', () => {
		Swal.fire({
			title: 'Are you sure you want to contact agent?',
			showDenyButton: false,
			showCancelButton: true,
			confirmButtonText: 'Continue',
		  }).then((result) => {
			if (result.isConfirmed) {
				endpoint = '/send_notification'
				payload = JSON.stringify({
					"to": houseInfo.owner_id,
					"type": "inspection_request",
					"item_id": houseId,
				})
				request.post(endpoint, payload)
				.then(() => {
					showAlert("Agent has been contacted, you will be notified shortly", 'success')
				}).catch((err) => {
					errorHandler(err, "An error has occured");
				})
			} else if (result.isDenied) {}
		})
	})
}

// Book inspection button handler
async function bookInspection() {
	$("#book-ins-cont").on('click', () => {
		Swal.fire({
			icon: 'info',
        	title: 'You would be charged ₦1000?',
        	text: 'Which booking method would you prefer?',
			showDenyButton: true,
			denyButtonText: 'Physical booking',
			showCancelButton: true,
			confirmButtonText: 'Online booking',
		}).then((result) => {
			if (result.isConfirmed) {
				endpoint = '/book_inspection';
				var path = window.location.pathname;
				var queryString = window.location.search
				const callback_url = "" + path + queryString
				var payload = JSON.stringify({
					"callback_url": callback_url,
					"itemId": houseId
				})
				request.post(endpoint, payload)
				.then((auth_url) => {
					window.location.href = auth_url;
				}).catch((err) => {
					console.log(err)
					errorHandler(err, "Could not make payments now, please try again later");
				})
			} else if (result.isDenied) {
				endpoint = '/book_inspection';
				var payload = JSON.stringify({
					"itemId": houseId,
					"type": "physical"
				})
				request.post(endpoint, payload)
				.then((res) => {
					console.log("Physical payment scheduled");
					$("#contact-cont").removeClass('disappear');
					$("#inquiry-cont").html('');
					$("#uploader-phone").html(`<p class="contact"><icon class="fa fa-phone">
						<a href="tel:` + res.owner_phone + `" class="contact-links"> Call</a></icon></p>`)
					$("#uploader-whatsapp").html(`<p class="contact"><icon class="fa fa-whatsapp">
						<a href="https://api.whatsapp.com/send?phone=` + res.owner_phone + `" class="contact-links"> Whatsapp</a></icon></p>`)
				}).catch((err) => {
					errorHandler(err, "Error encountered");
				})
			}
		})
	})
}

// verify the status of user transaction
async function verifyPayment() {
	endpoint = '/verify_payment/' + houseId;
	return request.get(endpoint)
	.then((res) => {
		if (res.message == true) {
			console.log("Payment made successfully");
			$("#contact-cont").removeClass('disappear');
			$("#inquiry-cont").html('');
			$("#uploader-phone").html(`<p class="contact"><icon class="fa fa-phone">
				<a href="tel:` + res.owner_phone + `" class="contact-links"> Call</a></icon></p>`)
			$("#uploader-whatsapp").html(`<p class="contact"><icon class="fa fa-whatsapp">
				<a href="https://api.whatsapp.com/send?phone=` + res.owner_phone + `" class="contact-links"> Whatsapp</a></icon></p>`)
		} else {
			console.log("Payment has not been completed");
		}
	}).catch((err) => {
		if (err.status === 401) {
			console.log("User not logged in");
		} else {
			console.log("An error has occured");
		}
	})
}

function loadImages() {
	var carousel = document.querySelector(".carousel"),
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

Promise.all([getHouseInfo()])
.then((houseInfo) => {
	Promise.all([getImages(houseInfo[0]), getApartmentInfo(houseInfo[0]), getOwnerDetail(houseInfo[0]),
				getReviews(houseInfo[0])])
	.then(() => {
		var loader = document.getElementById('preloader');
		if (loader != null) {
			loader.style.display = "none";
		}
	})
}).catch((err) => {
	errorHandler(err, "Apartment not found, please re-check the url");
})

