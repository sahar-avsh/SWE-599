$(document).ready(function() {
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



