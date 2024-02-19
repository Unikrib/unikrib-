#!/usr/bin/node

// Load owner details
$(function(){
    request.get('/user/profile')
    .then((owner) => {
        request.get('/environments/' + owner.com_res)
        .then((env) => {
            $('#profile-cont').html(`
                <div id="profile-pic-cont">
                    <img src="` + owner.avatar + `">
                </div>
                <div id="name-cont">
                    <p class="name">` + owner.first_name + ` ` + owner.last_name + ` <icon class='fa fa-check-circle' id="verified"></icon></p>
                    <p class="edit-icon"><a href="profile-edit-page.html"><icon class="fa fa-pencil"></icon></a></p>
                    <p class="community" id="community-select">` + env.name + `</p>
                    <p class="email"> <icon class="fa fa-envelope"></icon> ` + owner.email + `</p>
                </div>
                <div id="contact-cont">
                    <div id="uploader-phone">
                        <p class="contact"><icon class="fa fa-phone"><a href="tel:` + owner.phone_no + `" class="contact-links"> ` + owner.phone_no + `</a></icon></p>
                    </div>
                    <div id="uploader-whatsapp">
                        <p class="contact"><icon class="fa fa-whatsapp"><a href="https://api.whatsapp.com/send?phone=+234` + owner.phone_no + `"
                        class="contact-links"> ` + owner.phone_no + `</a></icon></p>
                    </div>
                </div>`
            )
            if (!owner.isVerified) {
                $("#verified").addClass('disappear');
            }
            var loader = document.getElementById('preloader');
            if (loader != null) {
                loader.style.display = "none";
            }
        })
    }).catch((err) => {
        errorHandler(err, "Could not load user details");
    })
})