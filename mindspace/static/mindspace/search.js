$(document).ready(function() {
    $("#id_filter_button").click(function() {
        $.ajax({
            url: $(this).attr('load-results-url'),
            type: 'GET',
            data: {
                keyword_query: $("#id-search-keyword").val(),
                owner_query: $("#id-search-owner").val(),
            },
            success: function(response) {
                $("#id_results").html("");
                $("#id_results").append(response);
            }
        });
    });

    $('body').keypress(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            $("#id_filter_button").click();
        }
    });
});