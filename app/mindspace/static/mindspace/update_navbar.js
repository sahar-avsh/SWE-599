$(document).ready(function() {

    $.ajax({
        type: 'GET',
        url: $("#id-notif").data("url"),
        success: function(response) {
            $("#id-notif").html(response.notifs);
        }
    });

    var path = window.location.pathname;

    if (path.indexOf("mindspace/dashboard") >= 0) {
        $("#id-dashboard").addClass("active");
    }
    else if (path === "/questions/") {
        $("#id-qna").addClass("active");
    } 
    else if (path.indexOf("notifications") >= 0) {
        $("#id-notifications").addClass("active");
    } 
});