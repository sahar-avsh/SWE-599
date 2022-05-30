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
        // $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-add-mindspace"><a class="nav-link" id="id-add-mindspace-link" href="/mindspace/create/">Create a Mindspace</a></li></div><div class="dropdown-detail" id="id-create-mindspace-form"></div>');
    } 
    // else if (path.indexOf("mindspace/timeline") >= 0) {
    //     $("#id-timeline").addClass("active");
    // } 
    else if (path.indexOf("mindspace/detail") >= 0) {
        var ms_id = path.split("/").filter(e => e).pop();
        // $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-update-mindspace"><a class="nav-link" id="id-update-mindspace-link" href="/mindspace/' + ms_id + '/update/">Update this Mindspace</a></li></div><div class="dropdown-detail" id="id-update-mindspace-form"></div>');
        // $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-delete-mindspace"><a class="nav-link" id="id-delete-mindspace-link" href="/mindspace/' + ms_id + '/delete/">Delete this Mindspace</a></li></div><div class="dropdown-detail" id="id-delete-mindspace-form"></div>');
        // $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-share-mindspace"><a class="nav-link" id="id-share-mindspace-link" href="/mindspace/' + ms_id + '/share/">Share this Mindspace</a></li></div><div class="dropdown-detail" id="id-share-mindspace-form"></div>');
        $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-ask-mindspace"><a class="nav-link" id="id-ask-mindspace-link" href="/questions/create/">Ask a Question</a></li></div><div class="dropdown-detail" id="id-ask-question-mindspace-form"></div>');
        $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-add-resource"><a class="nav-link" id="id-add-resource-link" href="/mindspace/' + ms_id + '/create-resource/">Create a Resource</a></li></div><div class="dropdown-detail" id="id-add-resource-form"></div>');
    }
    // else if (path.indexOf("resource-detail") >= 0) {
    //     var ids = path.replace(/[^0-9.]/g, " ").split(" ").filter(e => e);
    //     $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-update-resource"><a class="nav-link" id="id-update-resource-link" href="/mindspace/' + ids[0] + '/' + ids[1] + '/update-resource/">Update this Resource</a></li></div><div class="dropdown-detail" id="id-update-resource-form"></div>');
    //     $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-delete-resource"><a class="nav-link" id="id-delete-resource-link" href="/mindspace/' + ids[0] + '/' + ids[1] + '/delete/">Delete this Resource</a></li></div><div class="dropdown-detail" id="id-delete-resource-form"></div>');
    // }
    else if (path === "/questions/") {
        $("#id-qna").addClass("active");
        // $("#id-navbar-items").append('<div class="navbar-dropdown"><li class="nav-item" id="id-ask-question"><a class="nav-link" id="id-ask-question-link" href="/questions/create/">Ask a Question</a></li></div><div class="dropdown-detail" id="id-ask-question-form"></div>');
    } 
    else if (path.indexOf("notifications") >= 0) {
        $("#id-notifications").addClass("active");
    } 
    // else if (path.indexOf("profiles") >= 0) {
    //     $("#id-profile").addClass("active");
    //     var id = $("#id-profile").attr("data-id");
    //     if (path.indexOf("update") < 0) {
    //         $("#id-navbar-items").append('<li class="nav-item" id="id-update-profile"><a class="nav-link" href="/profiles/' + id + '/update">Update your Profile</a></li>');
    //     }
    // }
    
    //console.log(path);

});