let menuButtons = document.getElementsByClassName("menuButton");
let loginButton = $(".js-openLoginModal");
let signUpButton = $(".signUpButton");
let loginModal = document.getElementsByClassName("loginModal")[0];
let signUpModal = document.getElementsByClassName("signUpModal")[0];

if (window.matchMedia("(max-width: 700px)").matches) {
    for (let menuButton of menuButtons) {
        let navHeight = menuButton.nextElementSibling.offsetHeight;
        menuButton.nextElementSibling.style.maxHeight = 0;
        console.log(navHeight);
        menuButton.onclick = () => {
            // e.target.classList.toggle("accordeon");
            menuButton.nextElementSibling.classList.toggle("accordeon");
            if (menuButton.nextElementSibling.offsetHeight == 0) {
                menuButton.style.color = "#F0B90B";
                menuButton.children[0].style.transform = "rotate(0deg)";
                menuButton.children[0].style.filter = "grayscale(0%)";
                menuButton.nextElementSibling.style.maxHeight = navHeight + "px";
            } else {
                menuButton.style.color = "#5d5d5d";
                menuButton.children[0].style.transform = "rotate(-180deg)";
                menuButton.children[0].style.filter = "grayscale(100%)";
                menuButton.nextElementSibling.style.maxHeight = 0 + "px";
            }
        }
    }
}

if(window.location.hash === '#open_login_modal' ){
    loginModal.style.display = "block";
    window.location.hash = '';
}

loginButton.on('click', function() {
    loginModal.style.display = "block";
    console.log('lll')
})
loginModal.onclick = () => {
    loginModal.style.display = "none";
}
loginModal.children[0].onclick = (e) => {
    e.stopPropagation();
}

if (signUpButton) {
    signUpButton.on('click', function (){
        signUpModal.style.display = "block";
    })
}

signUpModal.onclick = () => {
    signUpModal.style.display = "none";
}
signUpModal.children[0].onclick = (e) => {
    e.stopPropagation();
}

$('.open-registration').on('click', function () {
    loginModal.style.display = "none";
    signUpModal.style.display = "block";
});

let registrationButton = $(".button-registration");
let urlRegistration = $('.signUpModal form').attr('action');

registrationButton.on("click", function () {
    let data = $('.signUpModal form').serialize();
    let $this = $(this);

    $.ajax({
        url: urlRegistration,
        method: 'POST',
        data: data,
        dataType: 'json',

        success: function (data) {
            document.location.replace(window.location.origin + data.url);
        },
        error: function (error) {
            if (error.responseJSON) {
                $this.closest('form').find('.error-field').text('');
                error.responseJSON.message.forEach(function (item) {
                    if (item[0] === "bool_field") {
                        $('.error-field.bool').text(`${item[1]}`)
                    } else {
                        $this.closest('form').find(`input[name=${item[0]}]`).next('.error-field').text(`${item[1]}`)
                    }
                })
            }
        }
    })
});

let loginButtonForm = $(".button-login");
let urlLogin = $('.loginModal form').attr('action');

loginButtonForm.on("click", function () {
    let data = $('.loginModal form').serialize();
    let $this = $(this);

    $.ajax({
        url: urlLogin,
        method: 'POST',
        data: data,
        dataType: 'json',

        success: function (data) {
            document.location.replace(window.location.origin + data.url);
        },
        error: function (error) {
            if (error.responseJSON) {
                $this.closest('form').find('.error-field').text('');
                error.responseJSON.message.forEach(function (item) {
                    $this.closest('form').find(`input[name=${item[0]}]`).next('.error-field').text(`${item[1]}`)
                })
            }
        }
    })
});

