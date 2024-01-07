$(document).ready(function(){
    $('#library_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            if(response.success) {
                $('#createLibraryModal').modal('hide');
                $('#library_form')[0].reset();

                location.reload();
            }
            else {
                $('#libraryBodyModal').html(response)
            }
        },
        error: function () {
            // Handle errors if any
            alert('Error submitting form');
        }
        });
    })
});