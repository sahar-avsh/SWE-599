$(document).ready(function() {
  $("#id_tagged_mindspace").change(function () {
    var url = $("#id-question-form").attr("data-resources-url");
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
});
