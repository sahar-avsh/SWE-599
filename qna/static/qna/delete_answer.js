$(document).on('click', '.delete', function(){
    let confirmation = confirm("Are you sure you want to remove this answer?");
    if (confirmation) {
        let object_id = $(this).attr('data-object-id');
        let url = $(this).attr('delete-answer-url');
        var answerUrl = $("#id-answer-list").attr("load-answers-url");
        var question = $("#id-create-answer-button").data("id");
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            url: url,
            data: {
                'answer': object_id
            },
            type: "POST",
            success: function(resp) {
                alert("Answer deleted");
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
    }
});