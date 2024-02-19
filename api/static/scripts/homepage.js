#!/usr/bin/node

$(function() {
	request.get('/count/houses?page=hp')
	.then((count) => {
		$('#stat1').text(count);
	}).catch(() => {
		$('#stat1').text('0');
	})

	request.get('/count/users')
	.then((count) => {
		$("#stat2").text(count['agent']);
		$("#stat3").text(count['vendor']);
		$('#stat4').text(count['sp']);
	}).catch((err) => {
		if (err.status_code === 500) {
			window.location.reload();
		}
		$("#stat2").text('0');
		$("#stat3").text('0');
		$('#stat4').text('0');
	})
	var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})