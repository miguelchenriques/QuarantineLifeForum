function addComment(comment) {
    const profile_url = $("#profileURL").val().replace("username", comment['owner_username']);
    const like_url = $("#commentLikeUrl").val();
    const csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    const pub_date = convertDate(comment['pub_date']);

    let html_string;
    html_string = `<div class="commentsArticle">
                            <div class="commentsTop">
                                <a href="${profile_url}"><img src="${comment['owner_image']}" alt="Avatar" class="avatar"></a>
                                <a href="${profile_url}">${comment['owner_username']}</a>
                                <a>${pub_date}</a>
                            </div>
                            <div class="commentsText">
                                <a>${comment['text']}</a>
                            </div>
                            <div class="commentsButtons">
                                    <form class="likeForm" method="post" action="${like_url}" name="Comment">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfmiddlewaretoken}">
                                        <input type="hidden" name="article_id" value="${comment['id']}">
                                        <input type="submit" class="like commentsLike"  value="">
                                    </form>
                                <p name="Comment${comment['id']}" class="numberPizzas commentsPizzas">0 Likes</p>
                            </div>
                        </div>
                        `;
    $("#commentsDiv").prepend(html_string);
};

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
            dataType: 'json',
            data: {
                post_id: post_id,
                text: comment_text,
                csrfmiddlewaretoken: this_.find('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                $('#commentInput').val('');
                addComment(data);
            }
        })
    })
})