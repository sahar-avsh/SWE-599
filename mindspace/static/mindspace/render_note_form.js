$("#id-create-note-button").click(function () {
    var url = $("#id-create-note-button").attr("note-form-url");

    $.ajax({
      url: url,
      success: function (data) {
        $("#form-fields").html(data);
      }
    });
    document.getElementById("id-form").style.display = "";
    document.getElementById("id-create-note-button").style.display = "none";
  });

  $("#id-cancel-note-form").click(function () {
    $("#form-fields").html("");
    document.getElementById("id-form").style.display = "none";
    document.getElementById("id-create-note-button").style.display = "";
  })