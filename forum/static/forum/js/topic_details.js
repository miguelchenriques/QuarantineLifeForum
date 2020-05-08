function close_new_post() {
    $(".createPost").css("display", "none")
}

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

    $(".createPost_form").submit(function (e) {
        e.preventDefault();

        if (!login_required()) return;

        const this_ = $(this);
        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            dataType: 'json',
            data: {
                topic_id: $("#createPost-topicId").val(),
                title: this_.find('#title_id').val(),
                text: this_.find('#text_id').val(),
                image: this_.find('#image_id').val(),
                video: this_.find('#video_id').val(),
                csrfmiddlewaretoken: this_.find('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                if (data['created']) {
                    create_post(data);
                    close_new_post();
                }
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



function create_post(post) {
    const post_url = $("#postURL").val().replace('1', post['id']);
    const like_url = $("#likeURL").val();
    const topic_url = $("#topicURL").val();
    const profile_url = $("#profileURL").val().replace('username', post['owner_username']);
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    const pub_date = convertDate(post['pub_date']);
    let html_content;

    if (post['image']) {
        html_content = `<img src="${post['image']}">`
    } else if (post['video']) {
        html_content = `
            <iframe src="${post['video']}">
            </iframe>`
    } else {
        html_content = `<p class="postText">${post['text']}</p>`
    }

    let html;
    html = `
<article class="detail_post-articles" value="${post_url}">
    <div class="toppost">
        <a href="${profile_url}"><img src="${post['owner_image']}" alt="Avatar" class="avatar"></a>
        <a href="${profile_url}">${post['owner_username']}</a>
        <a>posted in</a>
        <a href="${topic_url}">t/${post['topic']}</a>
        <a>${pub_date}</a>
    </div>
    <div class="textpost">
        <p class="postTitle">${post['title']}</p>
        ${html_content}
    </div>
    <div class="buttonspost">
        <form class="likeForm" method="post" action="${like_url}" name="Post">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
            <input type="hidden" name="article_id" value="${post['id']}">
            <input type="submit" class="like" value="">
        </form>
        <p name="Post${post['id']}" class="numberPizzas">0 Likes</p>
    </div>
</article>
`;

    $(".Posts-Section").prepend(html);
}
