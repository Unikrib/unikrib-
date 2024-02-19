#!/usr/bin/node

const queryString = window.location.search;
const queryParams = new URLSearchParams(queryString);
const userId = queryParams.get("reported");
// var userId = getWithExpiry('revieweeId');

$(function() {
    $('#subBtn').on('click', function() {
        const radioButtons = $(".radio-btn");
        var payload = {}
        for (let i = 0; i < radioButtons.length; i++) {
            if (radioButtons[i].checked) {
                topic = radioButtons[i].value
                payload['topic'] = topic;
                break;
            }
        }
        
        // console.log(topic.value)
        var description = $('#description').val()
        payload['description'] = description;
        payload['reported'] = userId;
        request.post('/reports', JSON.stringify(payload))
        .then(() => {
            showAlert("Report added succesfully", 'success')
            window.location.href = 'report-confirmpage.html'
        }).catch((err) => {
            errorHandler(err, "Error adding report");
        })
    })
    var loader = document.getElementById('preloader');
	if (loader != null) {
		loader.style.display = "none";
	}
})