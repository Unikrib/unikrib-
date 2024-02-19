#!/usr/bin/node
var email = getWithExpiry("email");

$(function() {
    $('#confirm-reset').on('click', function() {
        var f = $("#f").val();
        var s = $("#s").val();
        var t = $("#t").val();
        var fo = $("#fo").val();
        var code = "" + f + s + t + fo;

        url = '/users/confirm-reset-code';
        var payload = JSON.stringify({"code": code, "email": email});
        request.post(url, payload)
        .then(() => {
            window.location.href = 'change-password.html';
        }).catch((err) => {
            errorHandler(err, "Invalid code, please retry")
        })
    })
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})