$(document).ready(function(){
    $('#customer_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            if(response.success) {
                $('#createCustomerModal').modal('hide');
                $('#customer_form')[0].reset();

                location.reload();
            }
            else {
                $('#customerBodyModal').html(response)
                $('#libraryCustomerButton').hide();
            }
        },
        error: function () {
            // Handle errors if any
            alert('Error submitting form');
        }
        });
    })
});