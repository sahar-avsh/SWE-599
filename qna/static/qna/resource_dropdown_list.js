$("#id_tagged_mindspace").change(function () {
    var url = $("#question_form").attr("data-resources-url");
    var mindspaceId = $(this).val();

    $.ajax({
      url: url,
      data: {
        'mindspace': mindspaceId
      },
      success: function (data) {
        $("#id_tagged_resource").html(data);
      }
    });
  });