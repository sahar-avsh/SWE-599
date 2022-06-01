$(document).ready(function() {
    $(document).on("click", "#id-sharedmindspaces-button", function() {
        $("#id-mymindspaces-button").removeClass("active");
        $("#id-mymindspaces-button").addClass("disabled");

        $("#id-search-results-button").removeClass("active");
        $("#id-search-results-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".my-mindspaces").hide();
        $(".mindspace-search-results").hide();
        $(".shared-mindspaces").show();
    });

    $(document).on("click", "#id-mymindspaces-button", function() {
        $("#id-sharedmindspaces-button").removeClass("active");
        $("#id-sharedmindspaces-button").addClass("disabled");

        $("#id-search-results-button").removeClass("active");
        $("#id-search-results-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".shared-mindspaces").hide();
        $(".mindspace-search-results").hide();
        $(".my-mindspaces").show();
    });

    $(document).on("click", "#id-search-results-button", function() {
        $("#id-sharedmindspaces-button").removeClass("active");
        $("#id-sharedmindspaces-button").addClass("disabled");

        $("#id-mymindspaces-button").removeClass("active");
        $("#id-mymindspaces-button").addClass("disabled");

        $(this).removeClass("disabled");
        $(this).addClass("active");

        $(".shared-mindspaces").hide();
        $(".my-mindspaces").hide();
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