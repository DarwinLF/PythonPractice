function attachLibrarySubmitHandler() {
    $('#library_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: '/libraries/library/createLibrary/modal/',
        data: $(this).serialize(),
        success: function(response) {
            if(response.status === 'success') {
                $('#createLibraryModal').modal('hide');
                $('#library_form')[0].reset();
                location.reload();
            }
            else {
                // Update the form with errors
                $('#libraryBodyModal').html(response.errors);
                attachLibrarySubmitHandler();
            }
        },
        error: function (error) {
            // Handle the error response
            if (error.responseJSON && error.responseJSON.status === 'error') {
                // Update the form with errors
                $('#libraryBodyModal').html(error.responseJSON.errors);
                attachLibrarySubmitHandler();
            }
        }
        });
    })
}

$(document).ready(function(){
    attachLibrarySubmitHandler();
});