$(document).ready(function () {
    $("#new_comment").submit(function (e) {
        e.preventDefault();
        const this_ = $(this);

        if (!login_required()) return;

        const comment_text = $('#commentInput').val();
        const post_id = this_.find('input[name=post_id]').val();

        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            dataType: 'html',
            data: {
                post_id: post_id,
                text: comment_text,
                csrfmiddlewaretoken: this_.find('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                $('#commentInput').val('');
                $("#commentsDiv").prepend(data);
            }
        })
    })
})