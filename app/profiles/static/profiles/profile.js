$(document).ready(function() {
    $("#id-profile-link").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-profile-detail").html(response);
                $("#id-profile-detail").show();
            }
        });
    });

    $(document).on("submit", "#id-form-edit-profile", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            data: $(this).serialize(),
            url: $(this).attr("action"),
            success: function(response) {
                $.ajax({
                    type: 'GET',
                    url: $("#id-profile-link").attr("href"),
                    success: function(response) {
                        $("#id-profile-detail").html(response);
                        $("#id-profile-detail").show();
                    }
                });
            }
        });
    });

    $(document).click(function(e) {
        if (e.target.id != 'id-profile-detail' && !$('#id-profile-detail').find(e.target).length)
        {
            $("#id-profile-detail").hide();
        }
    });
});