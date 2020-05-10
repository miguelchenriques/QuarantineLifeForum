function open_login() {
    $(".login").css("display", "flex");
};


async function login_required() {
    const api_url = $("#login_required_url").val();

    let authenticated;
    const response = await fetch(api_url, {method: 'GET'});
    const json = await response.json();
    authenticated = json['is_authenticated'];

    if (!authenticated) {
        open_login();
    }
    ;
    return authenticated
};

$(document).ready(function () {
    $("#navloginbutton").click(function () {
        open_login()
    });

    $("#close").click(function () {
        $(".login").css("display", "none")
    });

    $("#signup").click(function () {
        $(".login-form").css("display", "none");
        $(".signup-form").css("display", "flex");
        $(".login-art").css("order", "1");
        $(".signup-art").css("display", "flex");
        $(".login-art").css("display", "none");
        $("#close").css("left", "revert");
        $("#close").css("right", "10px");
    });

    $("#signin").click(function () {
        $(".login-form").css("display", "flex");
        $(".signup-form").css("display", "none");
        $(".login-art").css("order", "2");
        $(".signup-art").css("display", "none");
        $(".login-art").css("display", "flex");
        $("#close").css("left", "10px");
        $("#close").css("right", "revert");
    })

    $(document).on("submit", ".likeForm", function (e) {
        e.preventDefault();
        let this_ = $(this);

        if (!login_required()) return;

        const type = this_.attr('name');

        $.ajax({
            url: this_.attr("action"),
            method: "Post",
            data: {
                article_id: this_.find("input[name=article_id]").val(),
                csrfmiddlewaretoken: this_.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                const id = data['article_id'];
                if (data['has_like']) {
                    this_.find("input:submit").addClass("liked");
                } else {
                    this_.find("input:submit").removeClass("liked");
                }
                $(`p[name=${type}${id}]`).text(`${data['like_count']} Like${data['like_count'] === 1 ? '' : 's'}`)
            }
        })
    });

    $(document).on('submit', '.delete-form', function (e) {
        e.preventDefault();
        const this_ = $(this);

        if (!login_required()) return;

        const id = this_.find("input[name=article_id]").val();
        const type = this_.find("input[name=type]").val();
        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            dataType: 'json',
            data: {
                id: id,
                csrfmiddlewaretoken: this_.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                if (data['deleted']) {
                    $(`#${id}${type}Article`).remove()
                }
            }
        })
    });

    $("#forumtitle").click(function () {
        location.href = $(this).attr('value')
    });

    $("#forumicon").click(function () {
        location.href = $(this).attr('value')
    });

    $(document).on('click', ".detail_post-articles", function (e) {
        if ($(e.target).is('input') || $(e.target).is("iframe") || $(e.target).parents('.share-element').length) return;
        location.href = $(this).attr('value')
    });

    $(".topicsearch").click(function (e) {
        location.href = $(this).attr('value')
    });

    $(".userssearch").click(function (e) {
        location.href = $(this).attr('value')
    });

});
