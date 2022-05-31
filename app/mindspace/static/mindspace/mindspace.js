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
                var id = $("[id*=id-mindspace-title]").attr("id").split("-").pop();
                $("#id_tagged_mindspace").val(id);
                $.ajax({
                    type: 'GET',
                    url: $("#question_form").attr("data-resources-url"),
                    data: {
                        mindspace: id
                    },
                    success: function(response) {
                        $("#id_tagged_resource").html(response);
                    }
                });
                $("#id-ask-question-mindspace-form").show();
            }
        });
    });

    $(document).on("submit", "#question_form", function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(response) {
                window.location.replace("/questions/");
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
        const progress_bar = document.getElementById('progress');
        var formData = new FormData();

        $.each($(this).serializeArray(), function(index, value) {
            formData.append(value['name'], value['value']);
        });

        var img_data = $('#image_field').get(0).files[0];
        var doc_data = $('#document_field').get(0).files[0];
        var vid_data = $('#video_field').get(0).files[0];
        if (img_data) {
            formData.append('image', img_data);
            $("#progress").show();
        } else if (doc_data) {
            formData.append('document', doc_data);
            $("#progress").show();
        } else if (vid_data) {
            formData.append('video', vid_data);
            $("#progress").show();
        }
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            enctype: 'multipart/form-data',
            xhr: function() {
                var xhr = new window.XMLHttpRequest();

                xhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        const percentProgress = (e.loaded / e.total) * 100;
                        console.log(percentProgress);
                        progress_bar.innerHTML = '<div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width:' + percentProgress + '%" aria-valuenow="' + percentProgress + '" aria-valuemin="0" aria-valuemax="100"></div>'
                    }
                });
                return xhr
            },
            success: function(response) {
                $("#progress").hide();
                window.location.reload();
                // $("#id-mindspace-edit").html("");
            }
        });
    });

    $(document).on("submit", "#id-form-edit-resource", function(e) {
        e.preventDefault();
        var formData = new FormData();

        $.each($(this).serializeArray(), function(index, value) {
            formData.append(value['name'], value['value']);
        });

        var img_data = $('#image_field').get(0).files[0];
        var doc_data = $('#document_field').get(0).files[0];
        var vid_data = $('#video_field').get(0).files[0];
        if (img_data) {
            formData.append('image', img_data);
        } else if (doc_data) {
            formData.append('document', doc_data);
        } else if (vid_data) {
            formData.append('video', vid_data);
        }
        
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            enctype: 'multipart/form-data',
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

    // $(document).on("submit", "#id-navbar-search", function(e) {
    //     e.preventDefault();
    //     window.location.replace($(this).attr("redirect-url"));
        
    //     $.ajax({
    //         type: 'GET',
    //         url: $(this).attr("action"),
    //         data: {
    //             keyword_query: $("#id-navbar-search-input").val()
    //         },
    //         success: function(response) {
    //             if (!$("#id-search-results-button").length) {
    //                 $(".section-buttons").append('<button type="button" id="id-search-results-button" class="btn btn-light btn-lg btn-block disabled">Search Results</button>')
    //             }
    //             $(".mindspace-search-results").html(response);
    //         }
    //     });
    // });
});