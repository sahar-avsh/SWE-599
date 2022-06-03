$(document).ready(function() {

    $(document).on("click", "#id-resource-created-by", function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
            },
            error: function(response) {
                console.log(response);
            }
        });
    });

    $(document).on("click", "#id-update", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
            },
            error: function(response) {
                $("#id-mindspace-modal-body").html('<div class="alert alert-primary" role="alert"> \
                You do not have permission to edit this Mindspace! \
                </div>');
            }
        });
    });

    $(document).on("click", "#id-delete", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
            },
            error: function(response) {
                $("#id-mindspace-modal-body").html('<div class="alert alert-primary" role="alert"> \
                You do not have permission to delete this Mindspace! \
                </div>');
            }
        });
    });

    $(document).on("click", "#id-share", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
            },
            error: function(response) {
                $("#id-mindspace-modal-body").html('<div class="alert alert-primary" role="alert"> \
                You do not have permission to share this Mindspace! \
                </div>');
            }
        });
    });

    $(document).on("click", "#id-add-resource-link", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
            }
        });
    });

    $(document).on("change", "#id_tagged_mindspace", function(e) {
        e.stopImmediatePropagation();
        console.log('questions');
        if ($("#question_form").length) {
            var url = $("#question_form").attr("data-resources-url");
        } else {
            var url = $("#id-question-form").attr("data-resources-url");
        }
        
        var mindspaceId = $(this).val();
    
        $.ajax({
            type: 'GET',
            url: url,
            data: {
                'mindspace': mindspaceId
            },
            success: function (data) {
                $("#id_tagged_resource").html(data);
            }
        });
    });

    $(document).on("click", "#id-ask-mindspace-link", function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-mindspace-modal-body").html(response);
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
                $('#id-mindspace-modal').modal('toggle');
                $('#question_form').trigger("reset");
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
                window.location.reload();
            },
            error: function(response) {
                $.each(response.responseJSON.error, function(key, value) {
                    $("#id-mindspace-modal-body").append('<div class="alert alert-warning" role="alert">' + value + '</div>');
                });
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
            }
        });
    });

    $(document).on("submit", "#id-form-edit-resource", function(e) {
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
            }
        });
    });
});