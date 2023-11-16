#!/usr/bin/node
const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
const userId = queryParams.get("id");

// load agent info
async function getAgentInfo() {
	return request.get('/user/profile')
	.then((owner) => {
		$('#profile-pic-cont').html('<img src="' + owner.avatar + '">')
		request.get('/environments/' + owner.com_res).then(
			(env) => {
				$('#name-cont').html(`<p class="name">` + owner.first_name + ` ` + owner.last_name + `  <icon class='fa fa-check-circle' id="verified"></icon></p>
					<p class="edit-icon"><a href="profile-edit-page.html"><icon class="fa fa-pencil"></icon></a></p>
					<p class="services" id="service-select">Agent</span></p>
					<p class="community2" id="community-select">` + env.name + `</p>
					<p class="rating"> ` + owner.rating.toFixed(1) + `</span><icon class="fa fa-star"></icon></span></p>
					<p class="bio">` + owner.note + `</p>`)
				if (!owner.isVerified) {
					$("#verified").addClass('disappear');
				}
			}
		)
	}).catch((err) => {
		errorHandler(err, "Could not load user info")
	})
}

// Load agent reviews
async function getReview() {
	$('#review-cont').html(`
		<p id="rev-headr">Latest review</p>
		<div id="latest-review-cont">
		</div>
		<div id="other-reviews-cont">
		<a href="review-page.html?id=` + userId + `">
			<p id="view-review"></p>
		</a>
		</div>`)
	return request.get('/users/' + userId + '/reviews')
	.then((reviews) => {
		if (reviews.length === 0){
			$('#latest-review-cont').html('<p id="review-message"> You have no reviews yet.</p>')
			$('#other-review-cont').addClass('disappear');
		} else {
			$("#other-reviews-cont").html(`
				<a href="review-page.html?id=` + userId + `">
				<p id="">View all reviews</p>
		  		</a>`)
			request.get('/users/' + reviews[0].reviewer)
			.then((reviewer) => {
				$('#latest-review-cont').html(`<div id="rev-img-cont">
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
	}).catch((err) => {
		errorHandler(err, "Could not load reviews");
	})
}

// Load agent apartments
async function getApartment() {
	return request.get('/users/me/houses')
	.then((houses) => {
		if (houses.length === 0) {
			$('#view-more-button').addClass('disappear')
			return;
		} else if (houses.length === 1) {
			$('#view-more-button').addClass('disappear')
		}
		$.each(houses, function(index, house){
			if (index === 0){
				var cont = "first-apart";
			} else {
				var cont = "view-more-cont";
			}
			request.get('/streets/' + house.street_id)
			.then((street) => {
				request.get('/environments/' + street.env_id)
				.then((env) => {
					$('#' + cont).append(`<div id="output-cont" class="output-containers">
						<div id="info-` + house.id + `" class ="value-links">
						<div id="image-cont">
						<img src="` + house.image1 + `" id="img10" class="apartment-img">
						</div>
						<div id="text-cont">
						<p class="address-results"><span class ="type">` + house.apartment + `</span> in <span class ="hostel" id="hostel10">` + house.name + ` </span>for rent
						<span class ="street" id="street10">` + street.name + ` street</span><span class ="community"  id="community10"> ` + env.name + `</span></p>
						<p class="price-results"><span class ="price" id="price10">N` + parsePrice(house.price) + ` </span>per year</p>
						<div class ="icons-cont">
						<i class="fa fa-tint"></i><i class="fa fa-trash"></i>
						</div>
						</div>
						</div>
						</div>`)
					$(function() {
						$('#info-' + house.id).on('click', function() {
							setWithExpiry('houseId', house.id);
							window.location.href = 'apartment-info-page2.html?id=' + house.id;
						})
					})
				})
			})
		})
	}).catch((err) => {
			errorHandler(err, "Could not load user apartments")
	})
}

Promise.all([getAgentInfo(), getReview(), getApartment()])
.then(() => {
	var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
}).catch((err) => {
	errorHandler(err, "Error loading page")
})
