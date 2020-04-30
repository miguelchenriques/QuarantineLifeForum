$(document).ready(function () {
    $("#login_form").on('submit', function (e) {
        e.preventDefault();
        let this_ = $(this);

        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            data: {
                username: $("#id_username").val(),
                password: $("#id_password").val(),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            dataType: "json",
            success: function (data) {
                if (data['login_successful']) {
                    location.reload();
                }
            }
        });

    })
});