var dropdown = document.querySelector('#dropdown');
var disp = document.getElementsByClassName('ph-disp');
var token = getWithExpiry('token');

class Requests {
    constructor() {
        // this.api = 'http://localhost:8000/unikrib';
        this.api = 'https://unikribafrica.com/unikrib'
        // this.api = 'https://unikribbackend-s0ik.onrender.com/unikrib';
    }

    get(endpoint) {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: 'GET',
                url: this.api + endpoint,
                contentType: 'application/json',
                headers: {
                    'Authorization': "unikrib " + token
                },
                crossDomain: true,
                dataType: 'json',
                success: function(data) {
                    resolve(data);
                },
                error: function(err) {
                    reject(err);
                }
            })
        })
    }

    postFile(payload) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: this.api + '/upload_image',
                type: 'POST',
                data: payload,
                headers: {
                    'Authorization': "unikrib " + token
                },
                processData: false,
                contentType: false,
                success: function(body) {
                    console.log(body)
                    resolve(body)
                },
                error: function(err) {
                    reject(err);
                }
            })
        })
    }

    post(endpoint, payload) {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: 'POST',
                url: this.api + endpoint,
                data: payload,
                contentType: 'application/json',
                headers: {
                    'Authorization': "unikrib " + token
                },
                dataType: 'json',
                success: function(data) {
                    resolve(data);
                },
                error: function(err) {
                    reject(err);
                }
            })
        })
    }

    put(endpoint, payload) {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: 'PUT',
                url: this.api + endpoint,
                data: payload,
                contentType: 'application/json',
                headers: {
                    'Authorization': "unikrib " + token
                },
                dataType: 'json',
                success: function(data) {
                    resolve(data);
                },
                error: function(err) {
                    reject(err);
                }
            })
        })
    }

    destroy(endpoint, payload=null) {
        return new Promise((resolve, reject) => {
            if (payload != null) {
                $.ajax({
                    type: 'DELETE',
                    url: this.api + endpoint,
                    contentType: 'application/json',
                    headers: {
                        'Authorization': "unikrib " + token
                    },
                    crossDomain: true,
                    dataType: 'json',
                    success: function(data) {
                        resolve(data);
                    },
                    error: function(err) {
                        reject(err);
                    }
                })
            } else {
                $.ajax({
                    type: 'DELETE',
                    url: this.api + endpoint,
                    contentType: 'application/json',
                    headers: {
                        'Authorization': "unikrib " + token
                    },
                    crossDomain: true,
                    dataType: 'json',
                    data: payload,
                    success: function(data) {
                        resolve(data);
                    },
                    error: function(err) {
                        reject(err);
                    }
                })
            }
        })
    }

    signin(email, password) {
        var payload = JSON.stringify({
            email,
            password,
        })
        return new Promise((res, rej) => {
            this.post('/auth/login', payload)
            .then((user) => {
                res(user);
            }).catch((err) => {
                rej(err)
            })
        })
    }

    signout() {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: 'DELETE',
                url: this.api + '/logout',
                contentType: 'application/json',
                headers: {
                    'Authorization': "unikrib " + token
                },
                dataType: 'json',
                success: function(data) {
                    resolve(data);
                },
                error: function(err) {
                    reject(err);
                }
            })
        })
    }
}

// Request function definitions
request = new Requests();

// Load top nav
if (token === null){
    // Not logged in
    $('#my-Top-nav').html(`
        <a href="homepage.html"><img src="images/Multi colo logo on transparent_2.png"></a>
        <a href="homepage.html">Home</a>
        <a href="Apartment-page.html">Apartments</a>
        <a href="product-page.html">Products</a>
        <a href="service-page.html">Services</a>

        <a id="login-sign">Login</a>
        <a id="login-signup">sign up</a>

        <a href="javascript:void(0);" class="icon" onclick="dropMenu()">
            <div class="icon-cont" onclick="changeIcon(this)">
                <div class="bar1"></div>
                <div class="bar2"></div>
                <div class="bar3"></div>
            </div>
         </a>`)
} else {
    // Logged in
    var first_name = getWithExpiry('first_name')
    var user_type = getWithExpiry('user_type')
    if (user_type === 'agent') {
        var postButton = '<a href="apartment-upload-page.html"><button class="upld">Post apartment</button></a>'
    } else if (user_type === 'vendor') {
        var postButton = '<a href="product-upload-page.html"><button class="upld">Post product</button></a>';
    } else if (user_type === 'sp') {
        var postButton = '<a href="service-image-edit-page.html"><button class="upld">Edit images</button></a>';
    } else {
        var postButton = ''
    }

    // populate the notif-badge with the number of unread messages
    request.get('/get_user_notifications')
    .then((nots) => {
        count = 0;
        for (var i=0; i<nots.length; i++) {
            if (!nots[i].read) {
                count++
            }
        }
        if (count > 0) {
            $("#not_length").text(count)
            $("#not_length").removeClass('disappear')
        }
    })

    $('#my-Top-nav').html(`
        <a href="homepage.html"><img src="images/Multi colo logo on transparent_2.png"></a>
        <a href="homepage.html">Home</a>
        <a href="Apartment-page.html">Apartments</a>
        <a href="product-page.html">Products</a>
        <a href="service-page.html">Services</a>
        ` + postButton + `
        
        <a class="ph-disp" onclick="getUserType()">Profile</a>
        <a id="help" class="ph-disp" onclick="help()">Help</a>
        <a class="ph-disp"><icon class="fa fa-user"></icon><span id="usr"> ` + first_name + `</span></a>
        <a class="ph-disp" id="logoff" onclick="logout()">Logout</a>

       
         <div class="dropdown" id="dropdown">
         <div class="notif-btn" id="notification"><i class="fa fa-bell">
          <span id="not_length" class="notif-badge disappear"></span>
          </i></div>
         
         <a href="javascript:void(0);" class="icon" onclick="dropMenu()">
         <div class="icon-cont" onclick="changeIcon(this)">
             <div class="bar1"></div>
             <div class="bar2"></div>
             <div class="bar3"></div>
         </div>
      </a>
          <button class="dropbtn" onclick="dropDown()"><icon class="fa fa-user"></icon> <icon class="fa fa-caret-down"></icon><span id="usr"> </span></buttons>
          <div class="dropmenu-content" id="dropdown-cont">
             <p class="drop-links" onclick="getUserType()">Profile</p>
             <p id="help" class="drop-links" onclick="help()">Help</p>
             <p class="drop-links" id="logoff" onclick="logout()">Logout</p>
         </div>
        </div>`)
}
$("#login-sign").on('click', function () {
    var path = window.location.pathname;
    var queryString = window.location.search
    const fullPath = "" + path + queryString
    setWithExpiry("path", fullPath);
    // window.location.assign('login.html')
    window.location.href = 'login.html';
});
$("#login-signup").on('click', function() {
    window.location.href = "agent-service-signup.html";
});
$("#notification").on('click', () => {
    window.location.href = "notification-page.html"
})

// Load footer nav
var footer = $("#footer-cont")
if (footer != null) {
    $("#footer-cont").html(`
        <div class="footer-sub-cont-a">
            <p ><a href="Apartment-page.html" class="foot-links">Apartments</a></p>
            <p><a href="product-page.html" class="foot-links">Products</a></p>
            <p><a href="service-page.html" class="foot-links">Services</a></p>
            <p><a href="about-page.html" class="foot-links">About us</a></p>
            <p><a href="agent-service-signup.html"class="foot-links">Become a unikrib agent, vendor or service provider</a></p>
        </div>
        <div class="footer-sub-cont-b">
            <p id="foot-para">For feedback and inquiries contact us on</p>
            <p><a href="tel:+2347054598108" class="foot-links"><i class="fa fa-phone" id="small1"></i>+2347054598108</a></p>
            <p></i><a href="https://api.whatsapp.com/send?phone=+2347041352299" class="foot-links"><i class="fa fa-whatsapp" id="small2"></i>+2347041352299</a</p>
            <p><i class="fa fa-envelope" id="small3"></i> <a href="mailto:unikrib@gmail.com?" class="foot-links">unikrib@gmail.com</a></p>
        </div>
        <div id="footer-base-cont">
            <div id="icon-cont">
                <div class="icon-sub-cont">
                    <a href="">
                    <img src="images/facebook-logo.png">
                    </a>
                </div>
                <div class="icon-sub-cont">
                    <a href="">
                    <img src="images/124021.png">
                    </a>
                </div>
                <div class="icon-sub-cont">
                    <a href="">
                    <img src="images/2048px-Instagram_icon.png">
                    </a>
                </div>
                <div class="icon-sub-cont">
                    <a href="">
                    <img src="images/official-linkedin-icon-png-16.jpg">
                    </a>
                </div>
            </div> 
        </div>`
    )
}

function help() {
    window.location.href = 'help-page.html'
}

function showEditProfile() {
    window.location.href = "profile-edit-page.html";
}

function getWithExpiry(key) {
	const itemStr = localStorage.getItem(key);
	if (!itemStr) {
		return null;
	}
	const item = JSON.parse(itemStr);
	const now = new Date()
	if (now.getTime() > item.expiry) {
		localStorage.removeItem(key)
		return null;
	}
    if (key === "path" || key === "error") {
        localStorage.removeItem(key);
    }
    // if (key != 'newId' || key != 'token') {
    //     localStorage.removeItem(key);
    // }
	return item.value;
}

function setWithExpiry(key, value) {
	const now = new Date()
    ttl = 24 * 60 * 60 * 1000 //one day

	const item = {
		value: value,
		expiry: now.getTime() + ttl,
	}
	localStorage.setItem(key, JSON.stringify(item))
}

// function setDict(key, values) {
//     localStorage.setItem(key, JSON.stringify(values))
// }

// function getDict(key) {
//     const items = localStorage.getItem(key)
//     // localStorage.removeItem(key)
//     return JSON.parse(items)
// }

function getUserType(){
    request.get('/user/profile')
    .then((currentUser) => {
        if (currentUser.user_type === 'agent'){
            window.location.href = 'agent-homepage.html?id=' + currentUser.id;
        } else if (currentUser.user_type === 'vendor') {
            window.location.href = 'vendor-homepage.html?id=' + currentUser.id;
        } else if (currentUser.user_type === 'sp'){
            window.location.href = 'service-homepage.html?id=' + currentUser.id;
        } else if (currentUser.user_type === 'regular'){
            window.location.href = 'user-homepage.html?id=' + currentUser.id;
        } else {
            alert("Could not determine user type")
        }
    }).catch((err) => {
        errorHandler(err, "Could not determine the user type")
    })
}

function readURL(input, position) {
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        document.querySelector('#' + position).setAttribute('src',e.target.result )
      };
      reader.readAsDataURL(input.files[0]);
    }
}

// var loader = document.getElementById('preloader');
// if (loader != null) {
//     window.addEventListener("load", function(){
//         loader.style.display = "none";
//     })
// }


function dropMenu() {
    var x = document.getElementById("my-Top-nav");
    if (x.className === "top-nav") {
        x.className += " responsive";
    } else {
        x.className  = "top-nav";
    }    
}

function logout(){    
    window.localStorage.clear();
    request.signout('/logout')
    .then(() => {
        window.location.href = 'homepage.html';
    }).catch((err) => {
        errorHandler(err, "Error signing out")
    })
    
}

function changeIcon(x) {
    x.classList.toggle("change");
}
function dropDown() {
    document.getElementById("dropdown-cont").classList.toggle("show");
}
window.onclick = function(e) {
    if(!e.target.matches(".dropbtn")) {
        var myDropdown =  document.getElementById("dropdown-cont");
        if (myDropdown != undefined){
            if (myDropdown.classList.contains("show")) {
                myDropdown.classList.remove("show");
            }
        }
    }
}

function showPassword(){
    var x = document.getElementById("input-pass");
    if(x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

function showToggle () {
    var icon = document.getElementById("eye-icon")
    icon.style.display="block";
}

function iconChange () {
    let x = document.getElementById("eye-icon");
    if (icon.className == "fa fa-eye") {
        icon.className = "fa fa-eye-slash";
    } else {
        icon.className = "fa fa-eye";
    }
}

// custom alert box
function showAlert(text, type) {
    // type === 'success' | 'info' | 'warning' | 'error'
    if (type === 'info' || type === 'warning') {
        var header = ''
    } else {
        var header = type
    }
    swal.fire({
        icon: type,
        title: header,
        text: text,
        showClass: {
            popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        }
    });
}

function showTimedAlert(text, type, timer) {
    swal.fire({
        icon: type,
        title: type,
        text: text,
        timer: timer,
        showConfirmButton: false,
        showClass: {
            popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        }
        // footer: "<a href='Apartment-page.html'>continue browsing unikrib</a>"
    });
}

function errorHandler(err, msg) {
    if (err.status === 401) {
        var path = window.location.pathname;
        var queryString = window.location.search
        const fullPath = "" + path + queryString
        window.localStorage.clear();
        setWithExpiry("path", fullPath);
        window.location.href = 'login.html';
        setWithExpiry("error", "Please log in or signup to continue");
        return;
    } else if (err.status === 500) {
        window.location.reload();
        return;
    }
    let icon = document.querySelector("#loader")
    if (icon != null) {
        icon.style.display="none";
    }
    if (err.responseJSON != undefined) {
        showAlert(err.responseJSON, 'error');
    } else {
        showAlert(msg, 'error');
    }
    return;
}
let button = $(".submit-btn")
if (button != null) {
    button.on("click", () => {
        if (button.hasClass('greyed') == true) {
            return;
        } else {
            let icon = document.querySelector("#loader")
            if (icon != null) {
                icon.style.display="block";
                button.addClass('greyed')
            }
        }
    })
}

let logoff = document.querySelector("#logoff")
if (logoff != null) {
    logoff.addEventListener("click", displayLogoff)
}

function displayLogoff() {
    let logoffloader = document.querySelector("#logoff-loader")
    logoffloader.style.display="grid";
}

let confirmbutton = document.querySelector(".cont-btn")
if (confirmbutton != null) {
    confirmbutton.addEventListener("click", showLoader)
}

function showLoader() {
    let iconloader = document.querySelector("#loader2")
    iconloader.style.display = "block";
}

function parsePrice(price) {
    let [integerPart, decimalPart] = price.toString().split('.');
    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

    const formattedPrice = decimalPart ? `${integerPart}.${decimalPart}` : integerPart;
    return formattedPrice;
}

function formatDatetime(inputDatetime) {
    const datetime = new Date(inputDatetime);
    const currentDate = new Date();
    
    const timeDifference = currentDate - datetime;
    const daysAgo = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    if (daysAgo === 0) {
        return "today"
    } else {
        return `${daysAgo} days ago`
    }
    // const daysAgoString = daysAgo === 0 ? 'today' : `${daysAgo} days ago`;
    
    // return daysAgoString;
}
