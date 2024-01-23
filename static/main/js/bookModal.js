function attachBookSubmitHandler() {
    $('#book_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: '/libraries/book/createBook/modal/',
        data: $(this).serialize(),
        success: function(response) {
            if(response.status === 'success') {
                $('#createBookModal').modal('hide');
                $('#book_form')[0].reset();
                location.reload();
            }
            else {
                $('#bookBodyModal').html(response.errors)
                $('#authorBookButton').hide();
                $('#libraryBookButton').hide();
                attachBookSubmitHandler();
            }
        },
        error: function () {
            // Handle errors if any
            if (error.responseJSON && error.responseJSON.status === 'error') {
                // Update the form with errors
                $('#bookBodyModal').html(error.responseJSON.errors);
                attachBookSubmitHandler();
            }
        }
        });
    })
}

$(document).ready(function(){
    attachBookSubmitHandler();
});