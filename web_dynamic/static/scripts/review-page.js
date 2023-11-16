#!/usr/bin/node

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
var reviewee = queryParams.get("id");
const userId = getWithExpiry('newId')

if (!reviewee) {
    var reviewee = getWithExpiry("revieweeId");
}

// Load user name
async function getUserName(){
    return request.get('/users/' + reviewee)
    .then((user) => {
        $('#fname').text(user.first_name + "'s");
        $('#fname2').text(user.first_name);
    }).catch((err) => {
        errorHandler(err, "Could not load owner name");
    })
}

// load all reviews for the user
async function getReviews(){
    return request.get('/users/' + reviewee + '/reviews')
    .then((reviews) => {
        $.each(reviews, function(index, review) {
            request.get('/users/' + review.reviewer)
            .then((reviewer) => {
                var star = parseInt(review.star)
                if (star >= 4) {
                    var code = 'positive'
                } else if(star == 3) {
                    var code = 'average'
                } else {
                    var code = 'poor'
                }
                $("#review-right-cont").append(`<div class="review-inbox">
                    <div class="reviewer-img-cont">
                        <img src="` + reviewer.avatar + `">
                    </div>
                    <div class ="reviewer-name-cont">
                        <p id="rev-name">` + reviewer.first_name + ` ` + reviewer.last_name + ` <icon class='fa fa-check-circle' id="verified-` + reviewer.id + `"></icon></p>
                    </div>
                    <div class="review-message-cont">
                        <p class="rev-message">` + review.text + `</p>
                        <div class="star-cont">
                            <p><span id="stars">` + review.star + `</span><icon class="fa fa-star" id="` + code + `"></icon></p>
                        </div>
                        <div class="time-stamp-cont">
                            <p class="time-stamp">` + review.updated_at.slice(0, 10) + `</p>
                        </div>
                    </div>
                </div>`)
                if (!reviewer.isVerified) {
                    $("#verified-" + reviewer.id).addClass('disappear');
                }
            })
        })
    }).catch((err) => {
        errorHandler(err, "Could not load user reviews");
    })
}

// Post new reviews
async function postNewReview(){
    $("#submit").on('click', function (){
        var payload = JSON.stringify({
            "star": $('#transact-rating :selected').val(),
            "text": $('#text').val(),
            "reviewee": reviewee,
        })
        $(function() {
            // send a notification to the reviewee
            var payload = JSON.stringify({"to": reviewee, "type": "new_review", "text": "A new review has been added for you"})
            var endpoint = '/send_notification'
            request.post(endpoint, payload)
        })
        return request.post('/reviews', payload)
        .then(() => {
            showAlert("Review added successfully", 'success')
            window.history.back();
        }).catch((err) => {
            errorHandler(err, "Failed to add review")
        })
    })
}

// check if user is eligible to add a review
async function checkEligibility() {
    var payload = JSON.stringify({
        "reviewee": reviewee,
        "reviewer": userId
    })
    return request.post('/review_eligibility', payload)
    .then((res) => {
        if (res.message === 'false') {
            $("#review-left-cont").addClass('disappear');
        }
    })
}

Promise.all([getUserName(), getReviews(), postNewReview()])     //, checkEligibility()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Failed to load page")
})