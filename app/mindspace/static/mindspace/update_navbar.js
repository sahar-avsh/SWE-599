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
    else if (path.indexOf("mindspace/detail") >= 0) {
        var ms_id = path.split("/").filter(e => e).pop();
        $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-ask-mindspace"><a class="nav-link" id="id-ask-mindspace-link" data-toggle="modal" data-target="#id-mindspace-modal" href="/questions/create/">Ask a Question</a></li></div>');
        $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-add-resource"><a class="nav-link" id="id-add-resource-link" data-toggle="modal" data-target="#id-mindspace-modal" href="/mindspace/' + ms_id + '/create-resource/">Create a Resource</a></li></div>');
    }
    else if (path === "/questions/") {
        $("#id-qna").addClass("active");
    } 
    else if (path.indexOf("notifications") >= 0) {
        $("#id-notifications").addClass("active");
    } 
});