    // function that hides/shows field_four based upon field_three value
    function check_field_value() {
        document.getElementById('div_id_video').style.display = 'none';
        document.getElementById('div_id_image').style.display = 'none';
        document.getElementById('div_id_document').style.display = 'none';
        document.getElementById('div_id_quote').style.display = 'none';
        document.getElementById('div_id_link').style.display = 'none';
        document.getElementById('video_field').style.display = 'none';
        document.getElementById('image_field').style.display = 'none';
        document.getElementById('document_field').style.display = 'none';
        document.getElementById('quote_field').style.display = 'none';
        document.getElementById('link_field').style.display = 'none';

        if($(this).val() === 'Video') {
            document.getElementById('div_id_video').style.display = '';
            document.getElementById('video_field').style.display = '';
            document.getElementById('div_id_link').style.display = '';
            document.getElementById('link_field').style.display = '';
        } else if ($(this).val() === 'Image') {
            document.getElementById('div_id_image').style.display = '';
            document.getElementById('image_field').style.display = '';
        } else if ($(this).val() === 'Document') {
            document.getElementById('div_id_document').style.display = '';
            document.getElementById('document_field').style.display = '';
        } else if ($(this).val() === 'Quote') {
            document.getElementById('div_id_quote').style.display = '';
            document.getElementById('quote_field').style.display = '';
        } else {
            document.getElementById('div_id_link').style.display = '';
            document.getElementById('link_field').style.display = '';
        }
    }

    // this is executed once when the page loads
    $(document).ready(function() {
        // set things up so my function will be called when res_format_field changes
        $('#res_format_field').change(check_field_value);

        // set the state based on the initial value
        check_field_value.call($('#res_format_field').get(0));
    });