#!/usr/bin/node

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);

var cat = queryParams.get("cat");
var pgsize = queryParams.get("pgsize", 4);
var pgnum = queryParams.get("pgnum", 1)
if (pgsize === null) {
	pgsize = 10;
}
if (pgnum === null) {
	pgnum = 1
}

//displays search parameters in search result heading
function searchParameter() {
    let community = $("#location-search :selected").text();
    let category = document.getElementById("product-category").value;
    let name = document.getElementById("product-search-box").value;
     document.getElementById("search-filter").innerHTML = 
     "Search results for " + name + " in " + community;
}

//changes the search button colour from green to purple
var buttons = document.getElementById("product-search");
buttons.addEventListener("click", changeColor)

function changeColor() {
    buttons.style.backgroundColor = "purple"
}

// Load all the available environments
async function getEnvironment(){
    return request.get('/environments')
    .then((environments) => {
        $.each(environments, function(index, env){
            if (env.name != "School hostel") {
                $('#location-search').append('<option value="' + env.id + '">' + env.name + '</option>')
            }
        })
    }).catch((err) => {
        errorHandler(err, "Could not load environments");
    })
}

// Load all the available categories
async function getCategory(){
    if (cat) {
        await request.get('/count/products?cat=' + cat)
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

        get_prods(total_pages, cat)
        .then(() => {
        }).catch((err) => {
            errorHandler(err, "Failed to fetch products in this category");
        })
    }
    return request.get('/categories')
    .then((cats) => {
        $.each(cats, function(index, cat){
            $('#product-category').append('<option value="' + cat.id + '">' + cat.name + '</option>');
            var url = 'product-page.html?cat=' + cat.id + '&pgsize=' + pgsize + '&pgnum=1&avail=yes'
            $('#Category').append('<a href="' + url + '" class="categories">' + cat.name + '</a>')
        })
    }).catch((err) => {
        errorHandler(err, "could not load available categories")
    })
}

function get_prods(total_pages, cat=null) {
    if (!cat) {
        var query = '/products?available=yes';
    } else {
        var query = '/categories/' + cat + '/products?available=yes'
    }
    query += "&pgnum=" + pgnum + "&pgsize=" + pgsize;

    return new Promise((res, rej) => {
        request.get(query)
        .then((products) => {
            load_prods(products, total_pages, cat)
            res(products);
        }).catch((err) => {
            rej(err);
        })
    })
}

function load_prods(prods, total_pages, cat=null) {
    if (prods.length === 0) {
        return;
    }

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
        var aft = pgnum + 1
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

    if (pgnum == total_pages) {
        $('#next').addClass('nav-btn-inactive');
    }
    if (pgnum == 1) {
        $("#prev").addClass('nav-btn-inactive');
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
    $.each(prods, function(_index, prod){
        request.get('/users/' + prod.owner_id)
        .then((owner) => {
            request.get('/environments/' + owner.com_res)
            .then((env) => {
                $('#product-list').append(`<div id="output-cont" class="output-containers">
                    <div id="` + prod.id + `">
                    <div id="image-cont">
                        <img src="` + prod.image1 + `" id="img1" class="product-imgs">
                    </div>
                    <div id="text-cont">
                        <p class="product-results"><span class="product-name">` + prod.name + ` </span></p>
                        <p class="price-results"><span class="product-price" id="product-price-1">₦` + parsePrice(prod.price) + `</span></p>
                        <p class="ven-location">Vendors location: <span class="community">` + env.name + `</span></p>
                        <span class="deliv">Delivery available</span></p>
                        <div class="view-btn-o">View product</div>
                    </div>
                    </div>
                </div>`)
                $(function (){
                    $("#" + prod.id).on('click', function(){											
                        window.location.href = 'product-info-page.html?id=' + prod.id;
                    });
                });
            })
        })
    })
}

// Load all the available products
async function getProducts(){
    if (!cat) {
        await request.get('/count/products')
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

        return get_prods(total_pages)
        .then(() => {
        }).catch((err) => {
            errorHandler(err, "Could not load available products");
        })
    }
}

// Load search results
async function getSearchResult(){
    $('#product-search').on('click', function(){
        var payload = JSON.stringify({
            "location": $('#location-search :selected').val(),
            "category": $('#product-category :selected').val(),
            "query": $('#product-search-box').val(),
        });
        return request.post('/product-search', payload)
        .then((products) => {
            showAlert('Search returned ' + products.length + ' results.', 'info')
            $('#product-list').html('')
            $("#nav-button-cont").html('')

            if (products.length === 0){
                $('#num-from').text('0');
                $('#num-to').text(products.length);
            } else {
                $('#num-from').text('1');
                $('#num-to').text(products.length);
            }
            $('#total-length').text(products.length);
            var total_pages = parseInt(parseInt($('#total-length').text()) / pgsize)
            if (parseInt($('#total-length').text()) % pgsize > 0) {
                total_pages += 1;
            }
            load_prods(products, total_pages);
        }).catch((err) => {
            errorHandler(err, "Could not load search results");
        })
    })
}

Promise.all([getEnvironment(), getCategory(), getProducts(), getSearchResult()])
.then(() => {
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})
.catch((err) => {
    errorHandler(err, "Failed to load page");
})