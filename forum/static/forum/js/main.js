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
    $(".likeForm").submit(function (e) {
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
                $(`p[name=${type}${id}]`).text(`${data['like_count']} Like${data['like_count'] === 1 ? '': 's'}`)
            }
        })
    });

    $("#forumtitle").click(function () {
        location.href = $(this).attr('value')
    })
});
