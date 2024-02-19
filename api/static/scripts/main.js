var login = document.querySelector('a.login-sign');
var signup = document.querySelector('a.login-signup');
var dropdown = document.querySelector('#dropdown');
var disp = document.getElementsByClassName('ph-disp');
var token = getWithExpiry('token');

class Requests {
    // Requests
    constructor() {
        // this.api = 'http://localhost:8000/unikrib';
        // this.api = 'https://unikribafrica.com/unikrib'
        this.api = 'https://unikribbackend-trhm.onrender.com/unikrib';
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



var help = document.getElementById('help')
if (help != undefined) {
    help.addEventListener("click", function() {
        window.location.href = 'help-page.html'
    })
}

var edit = document.getElementById('edit-profile')
if (edit != undefined) {
    edit.addEventListener("click", function() {
        window.location.href = "profile-edit-page.html";
    })
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
	return item.value;
}

function setWithExpiry(key, value) {
	const now = new Date()

    if (key === 'newId' || key === 'token') {
        ttl = 24 * 60 * 60 * 1000 //one day
    }
    else {
        ttl = 3 * 60 * 60 * 1000  //three hours
    }

	const item = {
		value: value,
		expiry: now.getTime() + ttl,
	}
	localStorage.setItem(key, JSON.stringify(item))
}

function getUserType(){
    request.get('/user/profile')
    .then((currentUser) => {
        if (currentUser.user_type === 'agent'){
            window.location.href = 'agent-homepage.html';
        } else if (currentUser.user_type === 'vendor') {
            window.location.href = 'vendor-homepage.html';
        } else if (currentUser.user_type === 'sp'){
            window.location.href = 'service-homepage.html';
        } else if (currentUser.user_type === 'regular'){
            window.location.href = 'user-homepage.html';
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

var loader = document.getElementById('preloader');
if (loader != null) {
    window.addEventListener("load", function(){
        loader.style.display = "none";
    })
}

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
    .then((resp) => {
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

function errorHandler(err, msg) {
    if (err.status === 401) {
        alert("Please log in to continue")
        window.location.href = 'login.html';
    }
    let icon = document.querySelector("#loader")
    if (icon != null) {
        icon.style.display="none";
    }
    if (err.responseJSON != undefined) {
        alert(err.responseJSON);
    } else {
        alert(msg)
    }
}
let button = document.querySelector(".submit-btn")
if (button != null) {
    button.addEventListener("click", displayLoader)
}

function displayLoader() {
   let icon = document.querySelector("#loader")
   icon.style.display="block";
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

