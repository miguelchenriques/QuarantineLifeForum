$(document).ready(function () {
    $(".likeForm").on("submit", function (e) {
        e.preventDefault();
        let this_ = $(this);

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
    })
});
