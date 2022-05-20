$(document).on('click', '.edit', function(){
    var id = $(this).attr("id");
    var counter = id.split('-');
    var uniq = counter[counter.length - 1];
    var url = $(this).attr("edit-answer-url");
    var answer = $(this).attr("data-object-id");
    var content = "id-answer-content-" + uniq;
    var edit = "id-edit-icon-" + uniq;
    var del = "id-delete-icon-" + uniq;
    
    $.ajax({
        url: url,
        data: {
            'answer_id': answer
        },
        success: function (data) {
            $("#" + content).html(data);
        }
    });
    document.getElementById(edit).style.display = "none";
    document.getElementById(del).style.display = "none";
});


$(document).on('click', '#id-cancel-button', function(e) {
    var question = $("#id-create-answer-button").data("id");
    var answerUrl = $("#id-answer-list").attr("load-answers-url");
    $.ajax({
        url: answerUrl,
        data: {
            'question': question
        },
        success: function(answerData) {
            $("#id-answer-list").html(answerData);
        }
    });
});

$(document).on('click', '#id-submit-button', function(e) {
    e.preventDefault();
    var answerUrl = $("#id-answer-list").attr("load-answers-url");
    var question = $("#id-create-answer-button").data("id");
    var actionUrl = $("#question_form").attr('action');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url: actionUrl,
        data: $("#question_form").serialize(),
        type: "POST",
        success: function(resp) {
            $.ajax({
                url: answerUrl,
                data: {
                    'question': question
                },
                success: function(answerData) {
                    $("#id-answer-list").html(answerData);
                }
            });
        },
        error: function(resp) {
            alert("Error");
        }
    });
});