$(document).ready(function () {
    $("#login_form").on('submit', function (e) {
        e.preventDefault();
        const this_ = $(this);

        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            data: {
                username: $("#id_username").val(),
                password: $("#id_password").val(),
                csrfmiddlewaretoken: $("#login_form input[name='csrfmiddlewaretoken']").val()
            },
            dataType: "json",
            success: function (data) {
                if (data['login_successful']) {
                    location.reload();
                }else{
                    $(".credencials-error").css("display", "block")
                    $(".login-form input:nth-child(-n+3)").css("border-bottom", "1px solid red")
                }
            }
        });
    })


    $("#signup_form").on('submit', function (e) {
        e.preventDefault();
        const this_ = $(this);

        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            data: {
                username: $("#signup_username").val(),
                email: $("#signup_email").val(),
                password1: $("#signup_password1").val(),
                password2: $("#signup_password2").val(),
                csrfmiddlewaretoken: $("#signup_form input[name='csrfmiddlewaretoken']").val()
            },
            dataType: "json",
            success: function (data) {
                if (data['signup_successful']) {
                    location.reload()
                }
            }
        })
    })
});