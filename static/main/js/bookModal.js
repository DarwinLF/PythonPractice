$(document).ready(function(){
    $('#book_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            if(response.success) {
                $('#createBookModal').modal('hide');
                $('#book_form')[0].reset();

                location.reload();
            }
            else {
                $('#bookBodyModal').html(response)
                $('#authorBookButton').hide();
                $('#libraryBookButton').hide();
            }
        },
        error: function () {
            // Handle errors if any
            alert('Error submitting form');
        }
        });
    })
});