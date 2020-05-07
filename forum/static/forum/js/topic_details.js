function open_createPost() {
        $(".createPost").css("display", "flex");
};

$(document).ready(function () {
    $("#topic-join").submit(function (e) {
        e.preventDefault();
        const this_ = $(this);

        if (!login_required()) return;

        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            dataType: 'json',
            data: {
                topic_id: $("#topic_id-join").val(),
                csrfmiddlewaretoken: this_.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                const num_followers = data['num_followers'];
                if (data['is_following']) {
                    $("#topic-join-submit").addClass('is_following')
                    $("#topic-join-submit").val('Following')
                } else {
                    $("#topic-join-submit").removeClass('is_following')
                    $("#topic-join-submit").val('Join')
                }
                $("#topic-followers").text(`${num_followers} Follower${num_followers === 1 ? '':'s'}`)
            }
        })
    });

    $("#createPost-button").click(function () {
        open_createPost()
    });
});
