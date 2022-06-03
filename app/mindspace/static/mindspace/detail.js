$(document).ready(function() {
    $(document).on("click", "#pills-resources-tab, #pills-questions-tab", function(e) {
        $(".spinner-border").show();
        var ms_id = window.location.pathname.split("/").filter(i => i).pop();
        var category = $(this).attr("id").split("-")[1];

        $.ajax({
            type: 'GET',
            url: $(this).data("url"),
            data: {
                'ms_id': ms_id,
                'category': category
            },
            success: function(response) {
                $("#pills-tabContent").html(response);
                $(".spinner-border").hide();
            },
            error: function(response) {
                console.log(response);
            }
        });
    });

    $(document).on("click", "[id*=id-mindspace-detail-items-page-]", function(e) {
        $(".spinner-border").show();
        e.preventDefault();
        e.stopImmediatePropagation();

        var url = $(this).attr("href");
        var page = $(this).attr("page-num");

        var is_viewing = $("#id-category").html();
        if (is_viewing === "resources") {
            var data = {'resources-page': page}
        } else if (is_viewing === "questions") {
            var data = {'questions-page': page}
        }

        data['ms_id'] = window.location.pathname.split("/").filter(i => i).pop();
        data['category'] = is_viewing;

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                $("#pills-tabContent").html(response);
                $(".spinner-border").hide();
                $("#pills-tabContent").show();
            },
            error: function(response) {
                console.log(response);
            }
        });
    });

    $(document).on("click", "a[id*=id-show-resource-detail]", function(e) {
        e.preventDefault();

        var element = document.getElementsByClassName("active-resource")[0];
        if (element) {
            element.classList.remove("active-resource");
            element.style.textDecoration = "none";
        }

        $(this).addClass("active-resource");
        $(this).css("text-decoration", "underline");
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-detail").html(response);
                $("#id-detail").css("background-color", "rgba(255, 248, 220, 0.815)");
                $("#id-collapse").show();
            }
        });
    });

    $(document).on("click", "#id-collapse", function() {
        $("#id-detail").html("");
        $(this).hide();
        $(".active-resource").css("text-decoration", "none");
        $(".active-resource").removeClass("active-resource");
    });

    $(document).on("click", "[id*=id-edit-resource-]", function() {
        $.ajax({
            type: 'GET',
            url: $(this).data("url"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
            },
            error: function(response) {
                $("#id-mindspace-modal-body").html('<div class="alert alert-primary" role="alert"> \
                You do not have permission to edit this Resource! \
                </div>');
            }
        });
    });

    $(document).on("click", "[id*=id-delete-resource-]", function() {
        $.ajax({
            type: 'GET',
            url: $(this).data("url"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
            },
            error: function(response) {
                $("#id-mindspace-modal-body").html('<div class="alert alert-primary" role="alert"> \
                You do not have permission to delete this Resource! \
                </div>');
            }
        });
    });
});



