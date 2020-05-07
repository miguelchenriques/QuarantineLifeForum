$(document).ready(function () {

    function open_createPost() {
        $(".createPost").css("display", "flex");
    };

    $("#createPost-button").click(function () {
        open_createPost()
    });

});