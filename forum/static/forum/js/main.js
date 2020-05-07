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
    $(".likeForm").on("submit", function (e) {
        e.preventDefault();
        let this_ = $(this);

        if (!login_required()) return;

        $.ajax({
            url: this_.attr("action"),
            method: "Post",
            data: {
                post_id: this_.find("input[name=post_id]").val(),
                csrfmiddlewaretoken: this_.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                const id = data['post_id']
                if (data['has_like']) {
                    this_.find("input:submit").addClass("liked");
                } else {
                    this_.find("input:submit").removeClass("liked");
                }
                if (data['like_count'] === 1) {
                    $("p[name="+id+"]").text(data['like_count']+" Like");
                } else {
                    $("p[name="+id+"]").text(data['like_count']+" Likes");
                }
            }
        })
    });

    $("#forumtitle").click(function () {
        location.href = $(this).attr('value')
    })

    $("#forumicon").click(function () {
        location.href = $(this).attr('value')
    })
});
