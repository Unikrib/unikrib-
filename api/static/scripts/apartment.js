#!/usr/bin/node

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
var payload = {}
if (queryParams.get('apartment')){
	payload['apartment'] = queryParams.get('apartment');
}
if (queryParams.get('min_price')){
	payload['min_price'] = queryParams.get('min_price');
}
if (queryParams.get('max_price')){
	payload['max_price'] = queryParams.get('max_price');
}
if (queryParams.get('environment')){
	payload['environment'] = queryParams.get('environment');
}
var search = queryParams.get("search");
var pgsize = queryParams.get("pgsize");
var pgnum = queryParams.get("pgnum")
if (pgsize === null) {
	pgsize = 10;
}
if (pgnum === null) {
	pgnum = 1
}

//load environments
async function getEnvironment() {
	return request.get('/environments')
	.then((envs) => {
		$.each(envs, function(index, env) {
			if (env.name != "School hostel") {
				$("#location-search").append("<option value='" + env.id + "'>" + env.name + "</option>");
			}
		});
	}).catch((err) => {
		errorHandler(err, "Could not load environments, please try again later");
	})
}


// Get apartments from server
function get_apartments(total_pages) {
	var query = '/houses?pgsize=' + pgsize + "&pgnum=" + pgnum
	$("#nav-button-cont").append(`
		<a href="` + window.location.pathname + `?pgsize=` + pgsize + `&pgnum=` + pgnum + `" class="nav-btn-active">` + pgnum + `</a>
	`)
	pgnum = parseInt(pgnum);
	if (pgnum == 1) {
		if (total_pages >= 2) {
			$("#nav-button-cont").append(`<a href="` + window.location.pathname + `?pgsize=` + pgsize + `&pgnum=2" class="nav-btn">2</a>`)
		}
		if (total_pages >= 3) {
			$("#nav-button-cont").append(`<a href="` + window.location.pathname + `?pgsize=` + pgsize + `&pgnum=3" class="nav-btn">3</a>`)
		}
	} else if (pgnum < total_pages) {
		var pre = pgnum - 1
		var aft = parseInt(pgnum) + 1
		$("#nav-button-cont").prepend(`<a href="` + window.location.pathname + `?pgsize=` + pgsize + `&pgnum=` + pre + `" class="nav-btn">` + pre + `</a>`)
		$("#nav-button-cont").append(`<a href="` + window.location.pathname + `?pgsize=` + pgsize + `&pgnum=` + aft + `" class="nav-btn">` + aft + `</a>`)
	}
	else if (pgnum == total_pages) {
		if (total_pages >= 2) {
			var pre = pgnum - 1
			$("#nav-button-cont").prepend(`<a href="` + window.location.pathname + `?pgsize=` + pgsize + `&pgnum=` + pre + `" class="nav-btn">` + pre + `</a>`)
		}
		if (total_pages >= 3) {
			var prepre = pre - 1
			$("#nav-button-cont").prepend(`<a href="` + window.location.pathname + `?pgsize=` + pgsize + `&pgnum=` + prepre + `" class="nav-btn">` + prepre + `</a>`)
		}
		// $("#next").addClass('nav-btn-inactive');
	}
	return new Promise((res, rej) => {
		request.get(query)
		.then((houses) => {
			$("#nav-button-cont").prepend('<a id="prev" class="nav-btn">&laquo Prev </a>');
			$("#nav-button-cont").append('<a id="next" class="nav-btn">Next &raquo</a>');
			if (pgnum == total_pages) {
				$('#next').addClass('nav-btn-inactive');
			}
			if (pgnum == 1) {
				$("#prev").addClass('nav-btn-inactive');
			}
			load_apartments(houses)
			res(houses);
		}).catch((err) => {
			rej(err);
		})
	})
}

// populate apartments in the page
function load_apartments(houses) {
	if (houses.length === 0) {
		return;
	}
	$("#next").on('click', function() {
		if (!$("#next").hasClass('nav-btn-inactive')) {
			var ne = parseInt(pgnum) + 1
			window.location.href = window.location.pathname + "?pgsize=" + pgsize + "&pgnum=" + ne
		}
	})
	$('#prev').on('click', function() {
		if (!$("#prev").hasClass('nav-btn-inactive')) {
			var ne = parseInt(pgnum) - 1
			window.location.href = window.location.pathname + "?pgsize=" + pgsize + "&pgnum=" + ne
		}
	})
	$.each(houses, function(_index, house) {
		request.get('/streets/' + house.street_id)
		.then((street) => {
			request.get('/environments/' + street.env_id)
			.then((env) => {
				$("#apartment-list").append(`
					<div id="output-cont" class="output-containers">
						<div id="info-` + house.id + `">
							<div id="image-cont">
								<img src="` + house.image1 + `" id="img1">
							</div>
							<div id="text-cont">
								<p class="address-results"><span class="type">` + house.apartment + `</span> in <span class="hostel" id="hostel1">` + house.name + `</span> for rent
								<span class ="street" id="street1">` + street.name + ` street,</span><span class ="community" id="community1"> ` + env.name + `</span></p>
								<p class="price-results"><span class="price" id="price1">₦` + parsePrice(house.price) + `</span> per year</p>
								<p id='commission-` + house.id + `' class='agent-fee'>Agent fee: <span  class='commision'></span></p>
								<div id="` + house.id + `-feats"></div>
								
								<div id='more-cont'>
								<div id='more-feat-cont'>
								<p id='units' class='more-feat'><i class='fa fa-home'></i><span> ` + house.rooms_available + ` </span>unit(s) available</p>
								<p id='built' class='more-feat'></p>
								<p id='security' class='more-feat'><span id=''></span></p>
								</div>
								<div id='more-info-cont'>
								<p id='time' class='more-info'><i class='fa fa-calendar'></i> posted: <span>` + formatDatetime(house.created_at) + `<span></p>
								<p id='' class='more-info'><span id='' class='views'><i class='fa fa-eye'> ` + house.no_clicks + `</i></span></P>
								</div>

								<div class="inspect-btn-o">Inspect</div>
							</div>
						</div>
					</div>
				`)
				if (house.agent_fee && house.agent_fee > 0) {
					$("#commission-" + house.id).text('Agent fee: ₦' + house.agent_fee)
				} else {
					// console.log(house.name + " has no agent fee");
					$("#commission-" + house.id).addClass('disappear');
				}
				var house_features = ""
				if (house.running_water === 'yes') {
					house_features += '<span class="feat">water</span>'
				}
				if (house.waste_disposal === 'yes') {
					house_features += '<span class="feat">waste disposal</span>'
				}
				if (house.tiled) {
					house_features += '<span class="feat">tiled</span>'
				}
				if (house.newly_built) {
					$("#built").text("Newly built");
				}
				if (house.security_available) {
					house_features += '<span class="feat">Security available</span>'
				}
				if (house.daily_power) {
					house_features += '<span class="feat">' + house.daily_power + 'hr power daily</span>'
				}
				$("#" + house.id + "-feats").html(house_features);
				$(function (){
					$("#info-" + house.id).on('click', function(){
						window.location.href = 'Apartment-info-page.html?id=' + house.id;
					});
				});
			})
		})
		
	})
	
}

// Load all apartments
async function getApartment() {
	if (search === "true") {
		return;
	}
	await request.get('/count/houses')
	.then((count) => {
		$('#total-length').text(count);
	}).catch(() => {
		if (err.statusCode == 500 || err.statusCode == 502) {
			window.location.reload()
		} else {
			$('#total-length').text('0');
		}
	})
	if (Object.keys(payload).length != 0) {
		return;
	}
	var total_pages = parseInt(parseInt($('#total-length').text()) / pgsize)
	if (parseInt($('#total-length').text()) % pgsize > 0) {
		total_pages += 1;
	}
	var num_to = pgnum * pgsize
	var num_from = num_to - pgsize + 1;
	if (num_to > parseInt($("#total-length").text())) {
		num_to = $("#total-length").text()
	}
	$("#num-to").text(num_to);
	$("#num-from").text(num_from);

	return get_apartments(total_pages)
	.then((houses) => {
	}).catch((err) => {
		console.log(err.toString())
		errorHandler(err, "Could not load apartments, please reload the page")
	})
}

// load search results
async function getSearchResult() {
	$("#button-cont").on('click', function() {
		var searchParams = {
			"apartment": $("#Apartment-type :selected").val(),
			"min_price": $("#minimum-price :selected").val(),
			"max_price": $("#maximum-price :selected").val(),
			"environment": $("#location-search :selected").val(),
		};
		var currentUrl = window.location.pathname;
		var queryStringParts = [];
		
		for (var key in searchParams) {
			if (searchParams.hasOwnProperty(key)) {
				var value = searchParams[key];
				queryStringParts.push(key + "=" + value);
			}
		}
		var queryString = queryStringParts.join("&");
		var newUrl = currentUrl + "?search=true&" + queryString + "&pgnum=" + pgnum + "&pgsize=" + pgsize;

		window.location.href = newUrl;
	})
}

async function loadSearchResult() {
	if (search != "true") {
		return;
	}
	var payload2 = JSON.stringify(payload);
	var url = '/houses/search?pgsize=' + pgsize;
	return request.post(url, payload2)
	.then((houses) => {
		$('#prev').addClass('nav-btn-inactive')
		showAlert("Search returned " + houses.length + " results", 'info');
		$('#total-length').text(houses.length);
		// if (pgnum == total_pages) {
		// 	$('#next').addClass('nav-btn-inactive');
		// }
		// if (pgnum == 1) {
		// 	$("#prev").addClass('nav-btn-inactive');
		// }
		if (houses.length === 0) {
			$("#num-from").text('0');
			$('#num-to').text('0');
			$('#next').addClass('nav-btn-inactive');
		} else {
			$("#num-from").text('1');
			$('#num-to').text(houses.length);
		}
		$("#apartment-list").html('');
		load_apartments(houses)
	}).catch((err) => {
		errorHandler(err, "Could not load search results now, please try again");
	})
}

// Get trending apartments
async function getTrendingApartments() {
	var endpoint = '/get-trending-apartments';
	return request.get(endpoint)
	.then((houses) => {
		if (houses.length === 0) {
			return;
		}
		$.each(houses, (_index, house) => {
			request.get('/streets/' + house.street_id)
			.then((street) => {
				request.get('/environments/' + street.env_id)
				.then((env) => {
					$("#slider-wrapper").append(`<div class="slider-cont" id="slide-a">
					<img src="` + house.image1 + `">
					<p><span id="">` + house.apartment + `</span> in <span id="">` + house.name + `,</span> <span id=""> ` + street.name + ` street</span> 
					<span id="">` + env.name + `</span></p>
					</div>`)
				})
			})
		})
	}).catch((err) => {
		console.log(err.toString())
	})
}

Promise.all([getEnvironment(), getApartment(), getSearchResult(), getTrendingApartments(), loadSearchResult()])
.then(() => {
	var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
}).catch((err) => {
	errorHandler(err, 'Failed to load page');
})
