if ($(".alert").length) {
    $(".alert").fadeTo(4000, 500).slideUp(500, function() {
        $(".alert").slideUp(500);
    });
}

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
        const progress_bar = document.getElementById('progress-profile');
        var formData = new FormData();
        $.each($(this).serializeArray(), function(index, value) {
            formData.append(value['name'], value['value']);
        });
    
        var img_data = $('#id_image').get(0).files[0];
        if (img_data) {
            formData.append('image', img_data);
            $("#progress-profile").show();
        }
        
        $.ajax({
            type: 'POST',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            enctype: 'multipart/form-data',
            url: $(this).attr("action"),
            xhr: function() {
                var xhr = new window.XMLHttpRequest();

                xhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        const percentProgress = (e.loaded / e.total) * 100;
                        console.log(percentProgress);
                        progress_bar.innerHTML = '<div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: ' + percentProgress + '%" aria-valuenow="' + percentProgress + '" aria-valuemin="0" aria-valuemax="100"></div>'
                    }
                });
                return xhr
            },
            success: function(response) {
                $.ajax({
                    type: 'GET',
                    url: $("#id-profile-link").attr("href"),
                    success: function(response) {
                        $("#id-profile-detail").html(response);
                        $("#progress-profile").hide();
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