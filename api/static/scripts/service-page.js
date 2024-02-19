#!/usr/bin/node

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
var cat = queryParams.get("cat")
var pgsize = queryParams.get("pgsize", 4);
var pgnum = queryParams.get("pgnum", 1)
if (pgsize === null) {
	pgsize = 10;
}
if (pgnum === null) {
	pgnum = 1
}

// Load all the available environments
async function getEnvironment(){
    return request.get('/environments')
    .then((envs) => {
        $.each(envs, function (index, env){
            if (env.name != "School hostel") {
                $('#community').append('<option value="' + env.id + '">' + env.name + '</option>')
            }
        })
    }).catch((err) => {
        errorHandler(err, "Could not load available environments");
    })
}

// Load all the available categories
async function getCategories(){
    if (cat != null) {
        await request.get('/count/services?cat=' + cat)
        .then((count) => {
            $('#total-length').text(count);
        })
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
        get_services(total_pages, cat)
        .then(() => {})
        .catch((err) => {
            errorHandler(err, "Failed to load services");
        })
    }
    return request.get('/service-categories')
    .then((cats) => {
        $.each(cats, function(index, cat){
            $('#service-provider').append('<option value="' + cat.id + '">' + cat.name + '</option>')
            $("#Category").append('<a href="service-page.html?cat=' + cat.id + '&pgsize=' + pgsize + '&pgnum=1" class="categories">' + cat.name + '</a>');
        })
    }).catch((err) => {
        errorHandler(err, "Error loading service categories");
    })
}

function get_services(total_pages, cat=null) {
    if (cat != null) {
        var query = '/service-categories/' + cat + '/services';
    } else {
        var query = '/services'
    }
    query += "?pgnum=" + pgnum + "&pgsize=" + pgsize;
    $("#nav-button-cont").append(`
		<a href="` + window.location.pathname + `?cat=` + cat + `&pgsize=` + pgsize + `&pgnum=` + pgnum + `" class="nav-btn-active">` + pgnum + `</a>
	`)
    if (cat != null) {
        var catQuery = '?cat=' + cat;
    } else {
        var catQuery = '?';
    }
    pgnum = parseInt(pgnum);
	if (pgnum == 1) {
		if (total_pages >= 2) {
			$("#nav-button-cont").append(`<a href="` + window.location.pathname + catQuery + `&pgsize=` + pgsize + `&pgnum=2" class="nav-btn">2</a>`)
		}
		if (total_pages >= 3) {
			$("#nav-button-cont").append(`<a href="` + window.location.pathname + catQuery + `&pgsize=` + pgsize + `&pgnum=3" class="nav-btn">3</a>`)
		}
	} else if (pgnum < total_pages) {
		var pre = pgnum - 1
		var aft = parseInt(pgnum) + 1
		$("#nav-button-cont").prepend(`<a href="` + window.location.pathname + catQuery + `&pgsize=` + pgsize + `&pgnum=` + pre + `" class="nav-btn">` + pre + `</a>`)
		$("#nav-button-cont").append(`<a href="` + window.location.pathname + catQuery + `&pgsize=` + pgsize + `&pgnum=` + aft + `" class="nav-btn">` + aft + `</a>`)
	} else if (pgnum == total_pages) {
		if (total_pages >= 2) {
			var pre = pgnum - 1
			$("#nav-button-cont").prepend(`<a href="` + window.location.pathname + catQuery + `&pgsize=` + pgsize + `&pgnum=` + pre + `" class="nav-btn">` + pre + `</a>`)
		}
		if (total_pages >= 3) {
			var prepre = pre - 1
			$("#nav-button-cont").prepend(`<a href="` + window.location.pathname + catQuery + `&pgsize=` + pgsize + `&pgnum=` + prepre + `" class="nav-btn">` + prepre + `</a>`)
		}
	}
    $("#nav-button-cont").prepend('<a id="prev" class="nav-btn">&laquo Prev </a>');
	$("#nav-button-cont").append('<a id="next" class="nav-btn">Next &raquo</a>');

    return new Promise((res, rej) => {
        request.get(query)
        .then((services) => {
            if (pgnum == total_pages) {
				$('#next').addClass('nav-btn-inactive');
			}
			if (pgnum == 1) {
				$("#prev").addClass('nav-btn-inactive');
			}
            load_services(services, cat)
            res(services);
        }).catch((err) => {
            rej(err);
        })
    })
}

function load_services(services, cat=null) {
    if (services.length === 0) {
        return;
    }
    $("#next").on('click', function() {
        if (!$("#next").hasClass('nav-btn-inactive')) {
            var ne = parseInt(pgnum) + 1
            if (cat) {
                window.location.href = window.location.pathname + "?pgnum=" + ne + "&pgsize=" + pgsize + "&cat=" + cat
            }
            else {
                window.location.href = window.location.pathname + "?pgnum=" + ne + "&pgsize=" + pgsize
            }
        }
    })
    $('#prev').on('click', function() {
        if (!$("#prev").hasClass('nav-btn-inactive')) {
            var pre = parseInt(pgnum) - 1
            if (cat) {
                window.location.href = window.location.pathname + "?pgnum=" + pre + "&pgsize=" + pgsize + "&cat=" + cat
            }
            else {
                window.location.href = window.location.pathname + "?pgnum=" + pre + "&pgsize=" + pgsize
            }
        }
    })
    $.each(services, function (_index, service) {
        request.get('/users/' + service.owner_id)
        .then((owner) => {
            request.get('/environments/' + owner.com_res)
            .then((env) => {
                request.get('/service-categories/' + service.category_id)
                .then((cat) => {
                    $("#service-list").append(`<div id="" class="output-containers">        
                            <div id="` + service.id + `">
                                <div id="img-container">
                                    <img src="` + service.image1 + `">
                                </div>
                                <div id="text-container">
                                    <p class ="name">` + owner.first_name + ` ` + owner.last_name + `</p>
                                    <p class="services" id="service-select"> ` + cat.name + `</p>
                                    <p class="community" id ="community-select">` + env.name + `</p>
                                    <div class="contact-btn-o">Contact</div>
                                    <p class="rating">Average star rating: <span class="ratings" id="rating-val-1">` + owner.rating.toFixed(1) + ` <icon class="fa fa-star"></icon></span></p>
                                </div>   
                            </div>
                        </div>`)

                    $(function (){
                        $("#" + service.id).on('click', function(){
                            window.location.href = 'service-info-page.html?id=' + service.id;
                        });
                    });
                })
            })
        })
    })
}

// Load all the available services
async function getServices(){
    if (cat) {
        return;
    }
    await request.get('/count/services')
    .then((count) => {
        $('#total-length').text(count);
    }).catch(() => {
        $('#total-length').text('0');
    })
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

    return get_services(total_pages)
    .then(() => {
    }).catch((err) => {
        errorHandler(err, "Could not load available services");
    })
}

// Load search results
async function getSearchResult(){
    $("#service-search").on('click', function(){
        var payload = JSON.stringify({
            "location": $('#community :selected').val(),
            "category_id": $('#service-provider :selected').val(),
        })
        catName = $('#service-provider :selected').text()
        return request.post('/service-search', payload)
        .then((services) => {
            showAlert("Search returned " + services.length + " results", 'info')
            $('#service-list').html('')
            if (services.length === 0){
                $('#num-from').text(0);
                $("#num-to").text(0)
            } else {
                $('#num-from').text(1);
                $("#num-to").text(services.length)
            }
            $('#total-length').text(services.length);
            load_services(services);
        })
    })
}

Promise.all([getEnvironment(), getCategories(), getServices(), getSearchResult()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Failed to load page");
})