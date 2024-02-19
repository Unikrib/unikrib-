#!/usr/bin/node

async function getNotifications() {
    request.get('/get_user_notifications')
    .then((nots) => {
        $.each(nots, function(_index, not) {
            if (not.read === true) {
                var status = 'read';
            } else {
                var status = 'unread'
            }

            if (not.category === 'inspection_request') {
                var text = `<p>` + not.text + `</p>`
                if (not.response === 'accepted') {
                    text += "<p><b>You accepted this request</b><p>";
                } else if (not.response === 'denied') {
                    text += "<p><b>You denied this request</b></p>";
                } else {
                    text += `<div id="button-cont-` + not.id + `" class="confirm-button-cont">
                            <button class="confirm-btn" id="accept-` + not.id + `">Available</button> <button class="delete-btn" id="deny-` + not.id + `">Unavailable</button>
                        </div>`
                }
            } else if (not.category === "inspection_accepted") {
                var text = '<p>' + not.text + '</p><p><a href="https://unikrib.com/static/Apartment-info-page.html?id=' + not.item_id + '">Contact agent</a></p>'
            } else if (not.category === "inspection_denied") {
                var text = '<p>' + not.text + '</p><p><a href="https://unikrib.com/static/Apartment-page.html">Check out more apartments</a></p>'
            } else {
                var text = '<p>' + not.text + '</p>'
            }
            $("#left-outer-container").append(
                `<div id="not-` + not.id + `" class="notification-div `+ status +`">
                    <div id="pic-cont"><img src="images/home-icon"class="notif-img"></div>
                    <div id="text-cont">` + text + `
                    </div>
                </div>`
            )
            // Accept request
            $(function () {
                $("#accept-" + not.id).on('click', function() {
                    var payload = JSON.stringify({
                        "to": not.sender,
                        "type": "inspection_accepted",
                        "item_id": not.item_id,
                        "not_id": not.id
                    })
                    var endpoint = '/send_notification';
                    request.post(endpoint, payload)
                    .then(() => {
                        showAlert("Thank you for your response", "success");
                        $("#accept-" + not.id).addClass('disappear');
                        $("#deny-" + not.id).addClass('disappear');
                        $("#button-cont-" + not.id).html("<b>You accepted this request</b>")
                    }).catch((err) => {
                        errorHandler(err, "An error occured and your response could not be sent");
                    })
                })
            })
            // Deny request
            $(function () {
                $("#deny-" + not.id).on('click', function() {
                    var payload = JSON.stringify({
                        "to": not.sender,
                        "type": "inspection_denied",
                        "item_id": not.item_id,
                        "not_id": not.id
                    })
                    var endpoint = '/send_notification';
                    request.post(endpoint, payload)
                    .then(() => {
                        showAlert("Thank you for your response, please delete the apartment if it is no longer available", "success");
                        $("#accept-" + not.id).addClass('disappear');
                        $("#deny-" + not.id).addClass('disappear');
                        $("#button-cont-" + not.id).html("<b>You denied this request</b>")
                    }).catch((err) => {
                        errorHandler(err, "An error occured and your response could not be sent");
                    })
                })
            })
            // mark notification as read when clicked
            $(function() {
                $("#not-" + not.id).on('click', function() {
                    if ($("#not-" + not.id).hasClass('unread')) {
                        $("#not-" + not.id).removeClass('unread');
                        $("#not-" + not.id).addClass('read');
                        var initial_count = parseInt($("#not_length").text())
                        if (initial_count === 1) {
                            $("#not_length").addClass('disappear')
                        } else {
                            $("#not_length").text(initial_count - 1);
                        }
                        var payload = JSON.stringify({"read": true})
                        request.put('/notifications/' + not.id, payload)
                    }
                })
            })
        })
    }).catch((err) => {
        errorHandler(err, "Error loading notification messages")
    })
}

Promise.all([getNotifications()])
.then(() => {})