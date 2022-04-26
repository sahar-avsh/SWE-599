$(document).ready(function(){
    var frm = $("#id-form");
    var resource = $("#id-create-note-button").data("id");

      frm.submit(function (e) {
        e.preventDefault();
        var actionUrl = $(this).attr('action');
        var noteUrl = $("#id-note-list").attr("load-notes-url");

        $.ajax({
          type: "POST",
          url: actionUrl,
          data: $(this).serialize(),
          success: function(data){
            $("#form-fields").html("");
            document.getElementById("id-form").style.display = "none";
            document.getElementById("id-create-note-button").style.display = "";
            //document.getElementById("id-note-list").style.display = "";
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
  })