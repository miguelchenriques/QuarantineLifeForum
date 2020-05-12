function close_new_post() {
    $(".createPost").css("display", "none")
}

$(document).ready(function () {
    $(".topic-join").submit(function (e) {
        e.preventDefault();
        const this_ = $(this);

        if (!login_required()) return;

        const id = this_.find(".topic_id-join").val()

        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            dataType: 'json',
            data: {
                topic_id: id,
                csrfmiddlewaretoken: this_.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                const num_followers = data['num_followers'];
                if (data['is_following']) {
                    this_.find(".topic-join-submit").addClass('is_following')
                    this_.find(".topic-join-submit").val('Following')
                } else {
                    this_.find(".topic-join-submit").removeClass('is_following')
                    this_.find(".topic-join-submit").val('Join')
                }
                $("#topic-followers"+id).text(`${num_followers} Follower${num_followers === 1 ? '' : 's'}`)
            }
        })
    });

    $(".createPost_form").submit(function (e) {
        e.preventDefault();

        if (!login_required()) return;

        const this_ = $(this);
        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            dataType: 'html',
            data: {
                topic_id: $("#createPost-topicId").val(),
                title: this_.find('#title_id').val(),
                text: this_.find('#text_id').val(),
                image: this_.find('#image_id').val(),
                video: this_.find('#video_id').val(),
                csrfmiddlewaretoken: this_.find('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                $(".Posts-Section").prepend(data);
                this_.find('#title_id').val('');
                this_.find('#text_id').val('');
                this_.find('#image_id').val('');
                this_.find('#video_id').val('');
                close_new_post();
            }
        })
    });


    $("#createPost-button").click(async function () {
        const auth = await login_required();
        if (!auth) return;

        $(".createPost").css("display", "flex");
    });

    $("#close_createComment").click(function () {
        close_new_post();
    });
});
