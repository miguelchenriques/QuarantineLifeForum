$(document).ready(function () {
    /* Faz o login utilizando AJAX */
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

    /*Faz o signUp utilizando AJAX*/
    $("#signup_form").on('submit', function (e) {
        e.preventDefault();
        const this_ = $(this);


        if ($("#signup_form #signup_username").hasClass("is_taken")
            || $("#signup_form signup_email").hasClass("is_taken")) {
            return;
        };

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
    });

    /* Valida o username */
    $("#signup_username").change(function () {
        const this_ = $(this);

        const url_username = $("input[name=url_usernameValidation]").val();
        $.ajax({
            url: url_username,
            method: "get",
            data: {
                username: this_.val()
            },
            dataType: 'json',
            success: function (data) {
                if (data['is_taken']) {
                    this_.addClass('is_taken')
                } else {
                    this_.removeClass('is_taken')
                }
            }
        })
    });

    /* Valida o email */
    $("#signup_email").change(function () {
        const this_ = $(this);

        const url_email = $("input[name=url_emailValidation]").val();
        $.ajax({
            url: url_email,
            method: "get",
            data: {
                username: this_.val()
            },
            dataType: 'json',
            success: function (data) {
                if (data['is_taken']) {
                    this_.addClass('is_taken')
                } else {
                    this_.removeClass('is_taken')
                }
            }
        })
    })
});


