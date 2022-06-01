$(document).ready(function() {
  $(document).on("click", "#id-create-note-button", function () {
    var url = $(this).attr("note-form-url");
    console.log(url);

    $.ajax({
      type: 'GET',
      url: url,
      success: function(response) {
        $("#id-note-create-container").html(response);
      }
    });
    document.getElementById("id-create-note-button").style.display = "none";
  });

  $(document).on('click', '#id-cancel-note-create-button', function(e) {
    document.getElementById("id-create-note-button").style.display = "";
    $("#id-note-create-container").html("");

  });

  $(document).on("submit", "#id-note-create-form", function(e) {
    e.preventDefault();
    var actionUrl = $(this).attr('action');
    var noteUrl = $("#id-note-list").attr("load-notes-url");
    var resource = $("#id-create-note-button").data("id");

    $.ajax({
      type: "POST",
      url: actionUrl,
      data: $(this).serialize(),
      success: function(data){
        $("#id-note-create-container").html("");
        document.getElementById("id-create-note-button").style.display = "";

        $.ajax({
          url: noteUrl,
          data: {
            'resource': resource
          },
          success: function(noteData) {
            $("#id-note-list").html(noteData);
          }
        });

      }

    });

  });

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
    document.getElementById("id-create-note-button").style.display = "none";
  });

  $(document).on('submit', '#id-note-update-form', function(e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    document.getElementById("id-create-note-button").style.display = "";
    var noteUrl = $("#id-note-list").attr("load-notes-url");
    var resource = $("#id-create-note-button").data("id");
    var actionUrl = $("#id-note-update-form").attr('action');

    $.ajax({
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

  $(document).on('click', '#id-cancel-note-update-button', function(e) {
    document.getElementById("id-create-note-button").style.display = "";
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

  $(document).on('click', '.delete', function(){
    let confirmation = confirm("Are you sure you want to remove this note?");
    if (confirmation) {
        let object_id = $(this).attr('data-object-id');
        let url = $(this).attr('delete-note-url');
        var noteUrl = $("#id-note-list").attr("load-notes-url");
        var resource = $("#id-create-note-button").data("id");
        $.ajax({
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
});