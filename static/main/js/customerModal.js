function attachCustomerSubmitHandler() {
    $('#customer_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: '/persons/customer/createCustomer/modal/',
        data: $(this).serialize(),
        success: function(response) {
            if(response.status === 'success') {
                $('#createCustomerModal').modal('hide');
                $('#customer_form')[0].reset();
                location.reload();
            }
            else {
                $('#customerBodyModal').html(response.errors)
                $('#libraryCustomerButton').hide();
                attachCustomerSubmitHandler();
            }
        },
        error: function () {
            // Handle errors if any
            if (error.responseJSON && error.responseJSON.status === 'error') {
                // Update the form with errors
                $('#customerBodyModal').html(error.responseJSON.errors);
                attachCustomerSubmitHandler();
            }
        }
        });
    })
}

$(document).ready(function(){
    attachCustomerSubmitHandler()
});