$(document).ready(function(){
    $('#author_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            if(response.success) {
            $('#createAuthorModal').modal('hide');
            $('#author_form')[0].reset();

            location.reload();
            }
            else {
            $('#authorBodyModal').html(response)
            }
        },
        error: function () {
            // Handle errors if any
            alert('Error submitting form');
        }
        });
    })
});