$(document).on('click', '.edit', function(){
    var id = $(this).attr("id");
    var counter = id.split('-');
    var uniq = counter[counter.length - 1];
    var url = $(this).attr("edit-note-url");
    var note = $(this).attr("data-object-id");
    var content = "id-note-content-" + uniq;
    var edit = "id-edit-icon-" + uniq;
    var del = "id-delete-icon-" + uniq;
    
    $.ajax({
        url: url,
        data: {
            'note_id': note
        },
        success: function (data) {
            $("#" + content).html(data);
        }
    });
    document.getElementById(edit).style.display = "none";
    document.getElementById(del).style.display = "none";
});


$(document).on('click', '#id-cancel-button', function(e) {
    var resource = $("#id-create-note-button").data("id");
    var noteUrl = $("#id-note-list").attr("load-notes-url");
    $.ajax({
        url: noteUrl,
        data: {
            'resource': resource
        },
        success: function(noteData) {
            $("#id-note-list").html(noteData);
        }
    });
});

$(document).on('click', '#id-submit-button', function(e) {
    e.preventDefault();
    var noteUrl = $("#id-note-list").attr("load-notes-url");
    var resource = $("#id-create-note-button").data("id");
    var actionUrl = $("#id-note-update-form").attr('action');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url: actionUrl,
        data: $("#id-note-update-form").serialize(),
        type: "POST",
        success: function(resp) {
            $.ajax({
                url: noteUrl,
                data: {
                    'resource': resource
                },
                success: function(noteData) {
                    $("#id-note-list").html(noteData);
                }
            });
        },
        error: function(resp) {
            alert("Error");
        }
    });
});