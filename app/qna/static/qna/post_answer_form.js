$(document).ready(function(){
    var frm = $("#id-form");
    var question = $("#id-create-answer-button").data("id");

      frm.submit(function (e) {
        e.preventDefault();
        var actionUrl = $(this).attr('action');
        var answerUrl = $("#id-answer-list").attr("load-answers-url");

        $.ajax({
          type: "POST",
          url: actionUrl,
          data: $(this).serialize(),
          success: function(data){
            $("#form-fields").html("");
            document.getElementById("id-form").style.display = "none";
            document.getElementById("id-create-answer-button").style.display = "";
            //document.getElementById("id-note-list").style.display = "";
            $.ajax({
              url: answerUrl,
              data: {
                'question': question
              },
              success: function(answerData) {
                $("#id-answer-list").html(answerData);
              }
            });
          }
        });
      });
  })