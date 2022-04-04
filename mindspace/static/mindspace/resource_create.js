
// Ideally this script (javascript code) would be in the HEAD of your page
// but if you put it at the bottom of the body (bottom of your template) that should be ok too.
// Also you need jQuery loaded but since you are using bootstrap that should
// be taken care of.  If not, you will have to deal with that.

    // function that hides/shows field_four based upon field_three value
    function check_field_value() {
        if($(this).val() == 'A Value') {
            // #id_field_four should be actually the id of the HTML element
            // that surrounds everything you want to hide.  Since you did
            // not post your HTML I can't finish this part for you.  
            $('#id_field_four').hide();
        } else {
            $('#id_field_four').show();
        }
    }

    // this is executed once when the page loads
    $(document).ready(function() {
        // set things up so my function will be called when field_three changes
        $('#id_field_three').change(check_field_value);

        // set the state based on the initial values
        check_field_value.call($('#id_field_three').get(0));
    });