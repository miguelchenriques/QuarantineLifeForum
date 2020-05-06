$(document).ready(function () {
    $("article").click(function (e) {
        if ($(e.target).hasClass('like')) return;
        location.href = $(this).attr('value')
    });

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
                } else {
                    $("#topic-join-submit").removeClass('is_following')
                }
            }
        })
    })
})
