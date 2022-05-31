// this method sends an ajax request to get question detail
// it adds a collapse icon
// Shows the answers div

function openQuestionDetail(id, url) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            // if ($(".comm-questions").is(":visible")) {
            //     $("#id-question-detail-" + id).html(response);

            //     if (!$("#id-collapse-question-detail-" + id).length) {
            //         $("#id-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
            //     }            
            // } 
            if ($(".my-questions").is(":visible")) {
                $("#id-myquestions-question-detail-" + id).html(response);

                if (!$("#id-collapse-myquestions-question-detail-" + id).length) {
                    $("#id-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-myquestions-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
                }            
            } 
            // else if ($(".my-answers").is(":visible")) {
            //     $("#id-myanswers-question-detail-" + id).html(response);

            //     if (!$("#id-collapse-myanswers-question-detail-" + id).length) {
            //         $("#id-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-myanswers-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
            //     }            
            // } 
            // else {
            //     $("#id-search-question-detail-" + id).html(response);

            //     if (!$("#id-collapse-search-question-detail-" + id).length) {
            //         $("#id-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-search-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
            //     }
            // }
        }
    });
}

function submitQuestionForm(url, data) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(response) {
            $(':input','#id-question-form')
            .not(':button, :submit, :reset, :hidden')
            .val('')
            .prop('checked', false)
            .prop('selected', false);
            $('#id-my-questions-button').trigger('click');
        }
    });
}

// Sends a GET ajax request to get answer form

function renderAnswerForm(id, url) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            if ($(".question-search-results").is(":visible")) {
                $("#id-search-question-answer-form-" + id).html(response);
                $("#id-search-question-answer-form-" + id).show();    
            } else if ($(".comm-questions").is(":visible")) {
                $("#id-question-answer-form-" + id).html(response);
                $("#id-question-answer-form-" + id).show();
            } else if ($(".my-questions").is(":visible")) {
                $("#id-myquestions-question-answer-form-" + id).html(response);
                $("#id-myquestions-question-answer-form-" + id).show();
            }
        }
    });
}

function loadAnswers(url, id) {
    $.ajax({
        type: 'GET',
        url: url,
        data: {
            'id': id
        },
        success: function(response) {
            if ($(".comm-questions").is(":visible")) {
                $("#id-main-answer-container-" + id).html(response);

                // update dummy ids
                $("*[id*=dummy-id-answer-edit-container]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-answer-edit-container-" + answer_id;
                });

                $("*[id*=dummy-id-rate-and-answer]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-rate-and-answer-" + answer_id;
                });
            } else if ($(".question-search-results").is(":visible")) {
                $("#id-search-main-answer-container-" + id).html(response);

                // update dummy ids
                $("*[id*=dummy-id-answer-edit-container]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-search-answer-edit-container-" + answer_id;
                });

                $("*[id*=dummy-id-rate-and-answer]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-search-rate-and-answer-" + answer_id;
                });
            } else if ($(".my-questions").is(":visible")) {
                $("#id-myquestions-main-answer-container-" + id).html(response);

                // update dummy ids
                $("*[id*=dummy-id-answer-edit-container]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-myquestions-answer-edit-container-" + answer_id;
                });

                $("*[id*=dummy-id-rate-and-answer]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-myquestions-rate-and-answer-" + answer_id;
                });
            } else {
                $("#id-myanswers-main-answer-container-" + id).html(response);

                // update dummy ids
                $("*[id*=dummy-id-answer-edit-container]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-myanswers-answer-edit-container-" + answer_id;
                });

                $("*[id*=dummy-id-rate-and-answer]").each(function() {
                    var answer_id = this.id.split("-").pop();
                    this.id = "id-myanswers-rate-and-answer-" + answer_id;
                });
            }
        }
    });
}

function postAnswerForm(url, data, q_id, answers_url) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(response) {
            if ($(".comm-questions").is(":visible")) {
                $("#id-question-answer-form-" + q_id).html("");
                $("#id-question-answer-form-" + q_id).hide();
            } else if ($(".question-search-results").is(":visible")) {
                $("#id-search-question-answer-form-" + q_id).html("");
                $("#id-search-question-answer-form-" + q_id).hide();
            } else if ($(".my-questions").is(":visible")) {
                $("#id-myquestions-question-answer-form-" + q_id).html("");
                $("#id-myquestions-question-answer-form-" + q_id).hide();
            }
            loadAnswers(answers_url, q_id);
        }
    });
}

function loadQuestionUpdateForm(url, id) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $("#id-myquestions-question-edit-container-" + id).html(response);
        }
    });
}

function loadQuestionDeleteForm(url, id) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $("#id-myquestions-question-edit-container-" + id).html(response);
        }
    });
}

function postQuestionUpdateForm(url, data, id, arrayData) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(response) {
            $("#id-question-title-" + id).html(arrayData[1]['value']);
            openQuestionDetail(id, response.url);
        }
    });
}

function postQuestionDeleteForm(url, data, id) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(response) {
            $("#id-myquestions-q-" + id).remove();
            $("#id-myquestions-question-detail-" + id).remove();
        }
    });
}

function loadAnswerUpdateForm(url, id) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            if ($(".my-answers").is(":visible")) {
                $("#id-myanswers-answer-edit-container-" + id).html(response);
                $("#id-myanswers-answer-edit-container-" + id).show();   
            } else if ($(".comm-questions").is(":visible")) {
                $("#id-answer-edit-container-" + id).html(response);
                $("#id-answer-edit-container-" + id).show();
            } else if ($(".my-questions").is(":visible")) {
                $("#id-myquestions-answer-edit-container-" + id).html(response);
                $("#id-myquestions-answer-edit-container-" + id).show();
            } else {
                $("#id-search-answer-edit-container-" + id).html(response);
                $("#id-search-answer-edit-container-" + id).show();
            }
        }
    });
}

function loadAnswerDeleteForm(url, id) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            if ($(".my-answers").is(":visible")) {
                $("#id-myanswers-answer-edit-container-" + id).html(response);
                $("#id-myanswers-answer-edit-container-" + id).show();   
            } else if ($(".comm-questions").is(":visible")) {
                $("#id-answer-edit-container-" + id).html(response);
                $("#id-answer-edit-container-" + id).show();
            } else if ($(".my-questions").is(":visible")) {
                $("#id-myquestions-answer-edit-container-" + id).html(response);
                $("#id-myquestions-answer-edit-container-" + id).show();
            } else {
                $("#id-search-answer-edit-container-" + id).html(response);
                $("#id-search-answer-edit-container-" + id).show();
            }
        }
    });
}

function postAnswerUpdateForm(url, data, id) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(response) {
            $.ajax({
                type: 'GET',
                url: response.url,
                success: function(response2) {
                    if ($(".comm-questions").is(":visible")) {
                        $("#id-answer-edit-container-" + id).html("");
                        $("#id-rate-and-answer-" + id).html(response2);
                    } else if ($(".my-answers").is(":visible")) {
                        $("#id-myanswers-answer-edit-container-" + id).html("");
                        $("#id-myanswers-rate-and-answer-" + id).html(response2);
                    } else if($(".my-questions").is(":visible")) {
                        $("#id-myquestions-answer-edit-container-" + id).html("");
                        $("#id-myquestions-rate-and-answer-" + id).html(response2);
                    }
                }
            });
        }
    });
}

function postAnswerDeleteForm(url, data) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(response) {
            loadAnswers(response.url, response.id);
        }
    });
}

// function loadMyAnswers(url) {
//     $.ajax({
//         type: 'GET',
//         url: url,
//         success: function(response) {
//             $(".own-answers").html(response);
//         }
//     });
// }

// sends an AJAX request to get My Answers section and makes it visible

function loadOwnAnswersSection(url) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $(".my-answers").html(response);
            $(".my-answers").show();
        }
    });
}

// sends an AJAX request to get My Questions section and makes it visible

function loadOwnQuestionsSection(url) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            $(".my-questions").html(response);
            $(".my-questions").show();
        }
    });
}

$(document).ready(function() {
    $(document).on("submit", "#id-question-form", function(e) {
        e.preventDefault();
        var url = $(this).attr("action");
        var data = $(this).serialize();
        submitQuestionForm(url, data);
    });

// Opens question details when clicked on the title - Covers Community Questions section

    $(document).on("click", "[id*=id-question-title-]", function(e) {
        var id = $(this).attr("id").split("-").pop();
        if ($(".comm-questions").is(":visible")) {
            $("#id-question-detail-" + id).show();

            if (!$("#id-collapse-question-detail-" + id).length) {
                $("#id-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
            }
        } else if ($(".my-answers").is(":visible")) {
            $("#id-myanswers-question-detail-" + id).show();

            if (!$("#id-collapse-myanswers-question-detail-" + id).length) {
                $("#id-myanswers-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-myanswers-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
            }
        } else if ($(".my-questions").is(":visible")) {
            $("#id-myquestions-question-detail-" + id).show();

            if (!$("#id-collapse-myquestions-question-detail-" + id).length) {
                $("#id-myquestions-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-myquestions-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
            }
        } else if ($(".question-search-results").is(":visible")) {
            $("#id-search-question-detail-" + id).show();

            if (!$("#id-collapse-search-question-detail-" + id).length) {
                $("#id-search-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-search-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
            }
        }
    });

// Collapses question details when clicked on the collapse icon - Covers Community Questions section

    $(document).on("click", "[id*=id-collapse-question-detail-]", function(e) {
        var id = $(this).attr("id").split("-").pop();
        $("#id-question-detail-" + id).hide();
        $(this).remove();
    });

// Collapses question details when clicked on the collapse icon - Covers My Answers section

    $(document).on("click", "[id*=id-collapse-myanswers-question-detail-]", function(e) {
        var id = $(this).attr("id").split("-").pop();
        $("#id-myanswers-question-detail-" + id).hide();
        $(this).remove();
    });

// Collapses question details when clicked on the collapse icon - Covers My Questions section

$(document).on("click", "[id*=id-collapse-myquestions-question-detail-]", function(e) {
    var id = $(this).attr("id").split("-").pop();
    $("#id-myquestions-question-detail-" + id).hide();
    $(this).remove();
});

// Collapses question details when clicked on the collapse icon - Covers Search Questions section

$(document).on("click", "[id*=id-collapse-search-question-detail-]", function() {
    var id = $(this).attr("id").split("-").pop();
    // $("#id-search-question-detail-" + id).html("");
    $("#id-search-question-detail-" + id).hide();
    // $("#id-search-question-answer-list-" + id).hide();
    $(this).remove();
});

// My questions button is clicked and that section is opened
// other sections are hidden

    $(document).on("click", "#id-my-questions-button", function() {
        $("#id-comm-button").removeClass("active");
        $("#id-comm-button").addClass("disabled");

        $("#id-my-answers-button").removeClass("active");
        $("#id-my-answers-button").addClass("disabled");

        $("#id-search-results-button").removeClass("active");
        $("#id-search-results-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".comm-questions").hide();
        $(".my-answers").hide();
        $(".question-search-results").hide();
        
        var url = $(this).data("url");
        loadOwnQuestionsSection(url);
    });

// My answers button is clicked and that section is opened
// other sections are hidden

    $(document).on("click", "#id-my-answers-button", function() {
        $("#id-comm-button").removeClass("active");
        $("#id-comm-button").addClass("disabled");

        $("#id-my-questions-button").removeClass("active");
        $("#id-my-questions-button").addClass("disabled");

        $("#id-search-results-button").removeClass("active");
        $("#id-search-results-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".comm-questions").hide();
        $(".my-questions").hide();
        $(".question-search-results").hide();
    
        var url = $(this).data("url");
        loadOwnAnswersSection(url);
    });

// My answers button is clicked and that section is opened
// other sections are hidden

    $(document).on("click", "#id-comm-button", function() {
        $("#id-my-questions-button").removeClass("active");
        $("#id-my-questions-button").addClass("disabled");

        $("#id-my-answers-button").removeClass("active");
        $("#id-my-answers-button").addClass("disabled");

        $("#id-search-results-button").removeClass("active");
        $("#id-search-results-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".my-questions").hide();
        $(".my-answers").hide();
        $(".question-search-results").hide();
        $(".comm-questions").show();
    });

    $(document).on("click", "#id-search-results-button", function() {
        $("#id-my-questions-button").removeClass("active");
        $("#id-my-questions-button").addClass("disabled");

        $("#id-my-answers-button").removeClass("active");
        $("#id-own-answers-button").addClass("disabled");

        $("#id-comm-button").removeClass("active");
        $("#id-comm-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".my-questions").hide();
        $(".my-answers").hide();
        $(".comm-questions").hide();
        $(".question-search-results").show();
    });

    $(document).on("click", "[id*=id-cancel-answer-form-]", function() {
        var id = $(this).attr("id").split("-").pop();
        if ($(".comm-questions").is(":visible")) {
            $("*[id*=id-question-answer-form-]:visible").each(function() {
                if (this.id.split("-").pop() === id) {
                    $("#" + this.id).html("");
                    $("#" + this.id).hide();
                }
            });
        } else if ($(".my-questions").is(":visible")) {
            $("*[id*=id-myquestions-question-answer-form-]:visible").each(function() {
                if (this.id.split("-").pop() === id) {
                    $("#" + this.id).html("");
                    $("#" + this.id).hide();
                }
            });
        }
    });

// Calls ajax GET to render answer form

    $(document).on("click", "[id*=id-add-answer-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        renderAnswerForm(id, url);
    });

    $(document).on("submit", "[id*=id-answer-form-]", function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var q_id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        var data = $(this).serialize();
        var answers_url = $(this).attr("load-answers-url");
        postAnswerForm(url, data, q_id, answers_url);
    });

    $(document).on("click", "[id*=id-myquestions-question-update-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        loadQuestionUpdateForm(url, id);
    });

    $(document).on("click", "[id*=id-myquestions-question-delete-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        loadQuestionDeleteForm(url, id);
    });

    $(document).on("click", "[id*=id-cancel-question-update-form-]", function() {
        var id = $(this).attr("id").split("-").pop();
        $("#id-myquestions-question-edit-container-" + id).html("");
    });

    $(document).on("click", "[id*=id-cancel-question-delete-form-]", function() {
        var id = $(this).attr("id").split("-").pop();
        $("#id-myquestions-question-edit-container-" + id).html("");
    });

    $(document).on("submit", "[id*=id-question-update-form-]", function(e) {
        e.preventDefault();
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        var data = $(this).serialize();
        var arrayData = $(this).serializeArray();
        postQuestionUpdateForm(url, data, id, arrayData);
    });

    $(document).on("submit", "[id*=id-question-delete-form-]", function(e) {
        e.preventDefault();
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        var data = $(this).serialize();
        postQuestionDeleteForm(url, data, id);
    });

    $(document).on("click", "[id*=id-answer-update-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        loadAnswerUpdateForm(url, id);
    });

    $(document).on("click", "[id*=id-answer-delete-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        loadAnswerDeleteForm(url, id);
    });

    $(document).on("submit", "[id*=id-answer-update-form-]", function(e) {
        e.preventDefault();
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        var data = $(this).serialize();
        postAnswerUpdateForm(url, data, id);
    });

    $(document).on("submit", "[id*=id-answer-delete-form-]", function(e) {
        e.preventDefault();
        var url = $(this).attr("action");
        var data = $(this).serialize();
        postAnswerDeleteForm(url, data);
    });

// Opens question details when clicked on title - Covers My Answers Section

    // $(document).on("click", "[id*=id-myanswers-question-title-]", function() {
    //     var id = $(this).attr("id").split("-").pop();
    //     if ($(".my-answers").is(":visible")) {
    //         $("#id-myanswers-question-detail-" + id).show();
    //     }
        
    //     if (!$("#id-collapse-myanswers-question-detail-" + id).length) {
    //         $("#id-myanswers-q-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-myanswers-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
    //     }
    // });

    $(document).on("click", "[id*=id-cancel-answer-update-form-]", function() {
        var id = $(this).attr("id").split("-").pop();
        if ($(".comm-questions").is(":visible")) {
            $("#id-answer-edit-container-" + id).html("");
            $("#id-answer-edit-container-" + id).hide();
        } else if ($(".my-answers").is(":visible")) {
            $("#id-myanswers-answer-edit-container-" + id).html("");
            $("#id-myanswers-answer-edit-container-" + id).hide();
        } else if ($(".question-search-results").is(":visible")) {
            $("#id-search-answer-edit-container-" + id).html("");
            $("#id-search-answer-edit-container-" + id).hide();
        } else {
            $("#id-myquestions-answer-edit-container-" + id).html("");
            $("#id-myquestions-answer-edit-container-" + id).hide();
        }
    });

    $(document).on("click", "[id*=id-cancel-answer-delete-form-]", function() {
        var id = $(this).attr("id").split("-").pop();
        if ($(".comm-questions").is(":visible")) {
            $("#id-answer-edit-container-" + id).html("");
            $("#id-answer-edit-container-" + id).hide();
        } else if ($(".my-answers").is(":visible")) {
            $("#id-myanswers-answer-edit-container-" + id).html("");
            $("#id-myanswers-answer-edit-container-" + id).hide();
        } else if ($(".question-search-results").is(":visible")) {
            $("#id-search-answer-edit-container-" + id).html("");
            $("#id-search-answer-edit-container-" + id).hide();
        } else {
            $("#id-myquestions-answer-edit-container-" + id).html("");
            $("#id-myquestions-answer-edit-container-" + id).hide();
        }
    });

    $(document).on("submit", "#id-question-search-form", function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        $.ajax({
            type: 'GET',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                $(".section-buttons").append('<button type="button" id="id-search-results-button" class="btn btn-light btn-lg btn-block disabled">Search Results</button>')
                $(".question-search-results").html(response);
            }
        });
    });

    $(document).on("click", "[id*=id-vote-]", function(e) {
        e.stopImmediatePropagation();
        var answer_id = $(this).attr("id").split("-").pop();
        var vote_type = $(this).attr("id").split("-")[2];

        $.ajax({
            type: 'POST',
            url: $(this).attr("action-url"),
            data: {
                'vote_type': vote_type,
                'answer_id': answer_id
            },
            success: function(response) {
                var score = parseInt($("#id-vote-score-" + answer_id).html());
                if (response.nature === "change" && response.vote === "U") {
                    $("#id-vote-score-" + answer_id).html(score + 2);
                } else if (response.nature === "change" && response.vote === "D") {
                    $("#id-vote-score-" + answer_id).html(score - 2);
                } else if (response.nature === "create" && response.vote === "U") {
                    $("#id-vote-score-" + answer_id).html(score + 1);
                } else if (response.nature === "create" && response.vote === "D") {
                    $("#id-vote-score-" + answer_id).html(score - 1);
                } else if (response.nature === "delete" && response.vote === "U") {
                    $("#id-vote-score-" + answer_id).html(score - 1);
                } else if (response.nature === "delete" && response.vote === "D") {
                    $("#id-vote-score-" + answer_id).html(score + 1);
                }
                $("#id-vote-icons-" + answer_id).html(response.vote_html);
            }
        });
    });

//     $(document).on("click", "[id*=id-search-question-title]", function() {
//         var id = $(this).attr("id").split("-").pop();
//         $.ajax({
//             type: 'GET',
//             url: $(this).data("url"),
//             success: function(response) {
//                 $("#id-search-question-detail-" + id).html(response);
//                 if (!$("#id-collapse-search-question-detail-" + id).length) {
//                     $("#id-q-search-" + id).append('<svg style="cursor: pointer; display: inline-block;" id="id-collapse-search-question-detail-' + id + '" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-bar-up" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 10a.5.5 0 0 0 .5-.5V3.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 3.707V9.5a.5.5 0 0 0 .5.5zm-7 2.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5z"/></svg>');
//                 }
//                 $("#id-search-question-answer-list-" + id).show();
//             }
//         });
//     });
});