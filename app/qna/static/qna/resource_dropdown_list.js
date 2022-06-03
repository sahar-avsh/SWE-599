$(document).ready(function() {

  $(document).on("change", "#id_tagged_mindspace_answer", function (e) {
    e.stopImmediatePropagation();
    var url = $("[id*=id-answer-form]:visible").attr("data-resources-url");
    if (!url) {
      var url = $("[id*=id-answer-update-form]:visible").attr("data-resources-url");
    }
    var mindspaceId = $(this).val();

    $.ajax({
      type: 'GET',
      url: url,
      data: {
        'mindspace': mindspaceId
      },
      success: function (data) {
        $("#id_tagged_resource_answer").html(data);
      }
    });
  });
});
