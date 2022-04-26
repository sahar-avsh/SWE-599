$(document).on('click', '.delete', function(){
    let confirmation = confirm("Are you sure you want to remove this note?");
    if (confirmation) {
        let object_id = $(this).attr('data-object-id');
        let url = $(this).attr('delete-note-url');
        var noteUrl = $("#id-note-list").attr("load-notes-url");
        var resource = $("#id-create-note-button").data("id");
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            url: url,
            data: {
                'note': object_id
            },
            type: "POST",
            success: function(resp) {
                alert("Note deleted");
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
    }
});

