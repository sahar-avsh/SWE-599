function loadQuestions(url, target) {
    if (target === "my-questions") {
        var data = {'my-questions-page': 1}
    } else if (target === "my-answers") {
        var data = {'my-answers-page': 1}
    } else if (target === "community-questions") {
        var data = {'community-questions-page': 1}
    }

    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        success: function(response) {
            $(".questions").html(response);
            $(".questions").show();
        },
        error: function(response) {
            console.log(response);
        }
    });
}

$(document).ready(function() {

    $(document).on("click", "[id*=id-question-page-]", function(e) {
        $(".spinner-border").show();
        e.preventDefault();
        e.stopImmediatePropagation();

        var url = $(this).attr("href");
        var page = $(this).attr("page-num");

        var is_viewing = $("#id-is-viewing").html();
        if (is_viewing === "community-questions") {
            var data = {'community-questions-page': page}
        } else if (is_viewing === "my-questions") {
            var data = {'my-questions-page': page}
        } else if (is_viewing === "my-answers") {
            var data = {'my-answers-page': page}
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                $(".questions").html(response);
                $(".spinner-border").hide();
                $(".questions").show();
            },
            error: function(response) {
                console.log(response);
            }
        });
    });

    $(document).on("click", "[id*=id-search-question-page-]", function(e) {
        $(".spinner-border").show();
        e.preventDefault();
        e.stopImmediatePropagation();

        var url = $(this).attr("href");
        var page = $(this).attr("page-num");
        var data = {'search-question-page': page}

        if ($("#id-keyword").length) {
            data['keyword'] = $("#id-keyword").html();
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                $(".spinner-border").hide();
                $(".question-search-results").html(response);
            },
            error: function(response) {
                console.log(response);
            }
        });
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

        // $(".comm-questions").hide();
        // $(".my-answers").hide();
        $(".question-search-results").hide();
        loadQuestions($(this).data("url"), "my-questions");
        // $(".my-questions").show();
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

        // $(".comm-questions").hide();
        // $(".my-questions").hide();
        $(".question-search-results").hide();
        loadQuestions($(this).data("url"), "my-answers");
        // $(".my-answers").show();
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

        // $(".my-questions").hide();
        // $(".my-answers").hide();
        $(".question-search-results").hide();
        loadQuestions($(this).data("url"), "community-questions");
        // $(".comm-questions").show();
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

        // $(".my-questions").hide();
        // $(".my-answers").hide();
        $(".questions").hide();
        $(".question-search-results").show();
    });

// Calls ajax GET to render answer form

    $(document).on("click", "[id*=id-add-answer-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                $(".modal-body").html(response);
            }
        });
    });

    $(document).on("click", "[id*=id-question-update-button-]", function(e) {
        e.stopImmediatePropagation();
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                $(".modal-body").html(response);
            }
        });
    });

    $(document).on("click", "[id*=id-question-delete-button-]", function(e) {
        e.stopImmediatePropagation();
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                $(".modal-body").html(response);
            }
        });
    });

    $(document).on("click", "[id*=id-answer-update-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                $(".modal-body").html(response);
            }
        });
    });

    $(document).on("click", "[id*=id-answer-delete-button-]", function() {
        var id = $(this).attr("id").split("-").pop();
        var url = $(this).attr("action");
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                $(".modal-body").html(response);
            }
        });
    });

    $(document).on("submit", "#id-question-search-form", function(e) {
        $(".spinner-border").show();
        e.preventDefault();
        e.stopImmediatePropagation();
        $.ajax({
            type: 'GET',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                if (!$("#id-search-results-button").length) {
                    $(".section-buttons").append('<button type="button" id="id-search-results-button" class="btn btn-light btn-lg btn-block disabled">Search Results</button>')
                }
                $(".question-search-results").html(response);
                $(".spinner-border").hide();
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
});