function attachAuthorSubmitHandler() {
    $('#author_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: '/persons/author/createAuthor/modal/',
        data: $(this).serialize(),
        success: function(response) {
            if(response.status === 'success') {
                $('#createAuthorModal').modal('hide');
                $('#author_form')[0].reset();
                location.reload();
            }
            else {
                $('#authorBodyModal').html(response.errors)
                attachAuthorSubmitHandler();
            }
        },
        error: function () {
            // Handle errors if any
            if (error.responseJSON && error.responseJSON.status === 'error') {
                // Update the form with errors
                $('#authorBodyModal').html(error.responseJSON.errors);
                attachAuthorSubmitHandler();
            }
        }
        });
    })
}

$(document).ready(function(){
    attachAuthorSubmitHandler()
});