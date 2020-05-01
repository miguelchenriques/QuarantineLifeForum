$(document).ready(function () {
    $(".likeForm").on("submit", function (e) {
        e.preventDefault();
        $.ajax({
        url: $(this).attr("action"),
        method: "Post",
        data: {
            post_id: $("input[name=post_id]").val(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function (data) {
            const id = data['post_id']
            $("p[name="+id+"]").text(data['like_count'])
        }
    })
    })
});


function toggle_like(this_) {

}