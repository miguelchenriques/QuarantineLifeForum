$(document).ready(function () {
    $(".likeForm").on("submit", function (e) {
        e.preventDefault();
        let this_ = $(this);
        toggle_like(this_);
    })
});


function toggle_like(this_) {
    $.ajax({
        url: this_.attr("action"),
        method: "Post",
        data: {
            post_id: this_.find("input[name=post_id]").val(),
            csrfmiddlewaretoken: this_.find("input[name=csrfmiddlewaretoken]").val()
        },
        success: function (data) {
            const id = data['post_id']
            $("p[name="+id+"]").text(data['like_count'])
            if (data['has_like']) {
                this_.find("input:submit").addClass("liked");
            } else {
                this_.find("input:submit").removeClass("liked");
            }

            if (data['like_count'] === 1) {
                this_.find(".like-span").text("Like");
            } else {
                this_.find(".like-span").text("Likes");
            }
        }
    })
}