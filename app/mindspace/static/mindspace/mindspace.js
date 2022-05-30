$(document).ready(function() {
    $("#id-add-mindspace-link").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-create-mindspace-form").html(response);
                $("#id-create-mindspace-form").show();
            }
        });
    });

    $("#id-update").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-edit").html(response);
                $("#id-mindspace-edit").css('border', '1px burlywood solid');
                //$("#id-update-mindspace-form").show();
            }
        });
    });

    $("#id-delete").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-edit").html(response);
                $("#id-mindspace-edit").css('border', '1px burlywood solid');
                // $("#id-delete-mindspace-form").show();
            }
        });
    });

    $("#id-share").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-edit").html(response);
                $("#id-mindspace-edit").css('border', '1px burlywood solid');
                //$("#id-share-mindspace-form").show();
            }
        });
    });

    $("#id-add-resource-link").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-add-resource-form").html(response);
                $("#id-add-resource-form").show();
            }
        });
    });

    // $("#id-update-resource-link").click(function(e) {
    //     e.preventDefault();
        
    //     $.ajax({
    //         type: 'GET',
    //         url: $(this).attr("href"),
    //         success: function(response) {
    //             $("#id-update-resource-form").html(response);
    //             $("#id-update-resource-form").show();
    //         }
    //     });
    // });

    // $("#id-delete-resource-link").click(function(e) {
    //     e.preventDefault();
        
    //     $.ajax({
    //         type: 'GET',
    //         url: $(this).attr("href"),
    //         success: function(response) {
    //             $("#id-delete-resource-form").html(response);
    //             $("#id-delete-resource-form").show();
    //         }
    //     });
    // });

    $("#id-ask-question-link").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-ask-question-form").html(response);
                $("#id-ask-question-form").show();
            }
        });
    });

    $("#id-ask-mindspace-link").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-ask-question-mindspace-form").html(response);
                $("#id_tagged_mindspace").val($("#id-profile").data("id"));
                // TODO: load the resources of this mindspace
                $("#id-ask-question-mindspace-form").show();
            }
        });
    });

    $(document).click(function(e) {
        if (e.target.id != 'id-create-mindspace-form' && !$('#id-create-mindspace-form').find(e.target).length)
        {
            $("#id-create-mindspace-form").hide();
        }

        // if (e.target.id != 'id-update-mindspace-form' && !$('#id-update-mindspace-form').find(e.target).length)
        // {
        //     $("#id-update-mindspace-form").hide();
        // }

        // if (e.target.id != 'id-delete-mindspace-form' && !$('#id-delete-mindspace-form').find(e.target).length)
        // {
        //     $("#id-delete-mindspace-form").hide();
        // }

        // if (e.target.id != 'id-share-mindspace-form' && !$('#id-share-mindspace-form').find(e.target).length)
        // {
        //     $("#id-share-mindspace-form").hide();
        // }

        if (e.target.id != 'id-add-resource-form' && !$('#id-add-resource-form').find(e.target).length)
        {
            $("#id-add-resource-form").hide();
        }

        if (e.target.id != 'id-update-resource-form' && !$('#id-update-resource-form').find(e.target).length)
        {
            $("#id-update-resource-form").hide();
        }

        if (e.target.id != 'id-delete-resource-form' && !$('#id-delete-resource-form').find(e.target).length)
        {
            $("#id-delete-resource-form").hide();
        }

        if (e.target.id != 'id-ask-question-form' && !$('#id-ask-question-form').find(e.target).length)
        {
            $("#id-ask-question-form").hide();
        }

        if (e.target.id != 'id-ask-question-mindspace-form' && !$('#id-ask-question-mindspace-form').find(e.target).length)
        {
            $("#id-ask-question-mindspace-form").hide();
        }
    });

    $(document).on("submit", "#id-create-mindspace-form", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                window.location.replace(response.nextURL);
            }
        });
    });

    $(document).on("submit", "#id-update-mindspace-form", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                window.location.reload();
            }
        });
    });

    $(document).on("submit", "#id-delete-mindspace-form", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                window.location.replace(response.nextURL);
            }
        });
    });

    $(document).on("submit", "#id-share-mindspace-form", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                // window.location.reload();
                $("#id-mindspace-edit").html("");
            }
        });
    });

    $(document).on("submit", "#id-create-resource-form", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                window.location.reload();
                // $("#id-mindspace-edit").html("");
            }
        });
    });

    $(document).on("submit", "#id-form-edit-resource", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                window.location.reload();
                // $("#id-mindspace-edit").html("");
            }
        });
    });

    $(document).on("submit", "#id-form-delete-resource", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                window.location.reload();
                // $("#id-mindspace-edit").html("");
            }
        });
    });
});