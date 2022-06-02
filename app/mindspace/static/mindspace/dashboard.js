function loadMindspaces(url, target) {
    if (target === "my-mindspaces") {
        var data = {'my-mindspace-page': 1}
    } else if (target === "shared-mindspaces") {
        var data = {'shared-mindspace-page': 1}
    }

    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        success: function(response) {
            $(".mindspace-lists").html(response);
            $(".mindspace-lists").show();
        },
        error: function(response) {
            console.log(response);
        }
    });
}

$(document).ready(function() {
    
    $(document).on("click", "[id*=id-mindspace-page-]", function(e) {
        $(".spinner-border").show();
        e.preventDefault();
        e.stopImmediatePropagation();

        var url = $(this).attr("href");
        var page = $(this).attr("page-num");

        var is_viewing = $("#id-is-viewing").html();
        if (is_viewing === "my-mindspace") {
            var data = {'my-mindspace-page': page}
        } else if (is_viewing === "shared-mindspace") {
            var data = {'shared-mindspace-page': page}
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                $(".mindspace-lists").html(response);
                $(".spinner-border").hide();
                $(".mindspace-lists").show();
            },
            error: function(response) {
                console.log(response);
            }
        });
    });

    $(document).on("click", "[id*=id-search-mindspace-page-]", function(e) {
        $(".spinner-border").show();
        e.preventDefault();
        e.stopImmediatePropagation();

        var url = $(this).attr("href");
        var page = $(this).attr("page-num");
        var data = {'search-mindspace-page': page}

        if ($("#id-keyword-query").length) {
            data['keyword_query'] = $("#id-keyword-query").html();
        }

        if ($("#id-owner-query").length) {
            data['owner_query'] = $("#id-owner-query").html();
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                $(".spinner-border").hide();
                $(".mindspace-search-results").html(response);
            },
            error: function(response) {
                console.log(response);
            }
        });
    });


    $(document).on("click", "#id-sharedmindspaces-button", function() {
        $("#id-mymindspaces-button").removeClass("active");
        $("#id-mymindspaces-button").addClass("disabled");

        $("#id-search-results-button").removeClass("active");
        $("#id-search-results-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".mindspace-search-results").hide();
        loadMindspaces($(this).data("url"), "shared-mindspaces");
    });

    $(document).on("click", "#id-mymindspaces-button", function() {
        $("#id-sharedmindspaces-button").removeClass("active");
        $("#id-sharedmindspaces-button").addClass("disabled");

        $("#id-search-results-button").removeClass("active");
        $("#id-search-results-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".mindspace-search-results").hide();
        loadMindspaces($(this).data("url"), "my-mindspaces");
    });

    $(document).on("click", "#id-search-results-button", function() {
        $("#id-sharedmindspaces-button").removeClass("active");
        $("#id-sharedmindspaces-button").addClass("disabled");

        $("#id-mymindspaces-button").removeClass("active");
        $("#id-mymindspaces-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".mindspace-lists").hide();
        $(".mindspace-search-results").show();
    });

    $(document).on("submit", "#id-mindspace-search-form", function(e) {
        $(".spinner-border").show();
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: $(this).attr("action"),
            data: {
                keyword_query: $("#id-search-keyword").val(),
                owner_query: $("#id-search-owner").val(),
            },
            success: function(response) {
                if (!$("#id-search-results-button").length) {
                    $(".section-buttons").append('<button type="button" id="id-search-results-button" class="btn btn-light btn-lg btn-block disabled">Search Results</button>')
                }
                $(".mindspace-search-results").html(response);
                $(".spinner-border").hide();
            }
        });
    });
});