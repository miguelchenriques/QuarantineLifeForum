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

const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function convertDate(date) {
    let [day, month, year, hour, minutes, AM_or_PM] = date.split('-');
    hour = AM_or_PM === 'PM' ? (parseInt(hour)-12).toString() : hour;
    month = monthNames[parseInt(month)-1];
    AM_or_PM = AM_or_PM === 'PM' ? 'p.m.' : 'a.m.';
    day = parseInt(day)

    return `${month} ${day}, ${year}, ${hour}:${minutes} ${AM_or_PM}`
}

$(document).ready(function () {
    $(document).on("submit",".likeForm", function (e) {
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

    $(document).on('submit', '.delete-form', function (e) {
        e.preventDefault();
        const this_ = $(this);

        if (!login_required()) return;

        const id = this_.find("input[name=article_id]").val();
        const type = this_.find("input[name=type]").val();
        $.ajax({
            url: this_.attr('action'),
            method: this_.attr('method'),
            dataType: 'json',
            data: {
                id: id,
                csrfmiddlewaretoken: this_.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                if (data['deleted']) {
                    $(`#${id}${type}Article`).remove()
                }
            }
        })
    });

    $("#forumtitle").click(function () {
        location.href = $(this).attr('value')
    });

    $("#forumicon").click(function () {
        location.href = $(this).attr('value')
    });

    $(document).on('click', ".detail_post-articles", function (e) {
        if ($(e.target).is('input') || $(e.target).is("iframe")) return;
        location.href = $(this).attr('value')
    });

    $(".topicsearch").click(function (e) {
        location.href = $(this).attr('value')
    });

    $(".userssearch").click(function (e) {
        location.href = $(this).attr('value')
    });

});
