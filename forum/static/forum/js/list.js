$(document).ready(function () {
    $("article").click(function (e) {
        if ($(e.target).hasClass('like')) return;
        location.href = $(this).attr('value')
    })
})
