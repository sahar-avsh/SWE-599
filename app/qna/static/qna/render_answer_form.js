$("#id-create-answer-button").click(function () {
    var url = $("#id-create-answer-button").attr("answer-form-url");

    $.ajax({
      url: url,
      success: function (data) {
        $("#form-fields").html(data);
      }
    });
    document.getElementById("id-form").style.display = "";
    document.getElementById("id-create-answer-button").style.display = "none";
  });

  $("#id-cancel-answer-form").click(function () {
    $("#form-fields").html("");
    document.getElementById("id-form").style.display = "none";
    document.getElementById("id-create-answer-button").style.display = "";
  })