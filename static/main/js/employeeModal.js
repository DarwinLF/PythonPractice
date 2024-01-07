$(document).ready(function(){
    $('#employee_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            if(response.success) {
                $('#createEmployeeModal').modal('hide');
                $('#employee_form')[0].reset();

                location.reload();
            }
            else {
                $('#employeeBodyModal').html(response)
                $('#libraryEmployeeButton').hide();
            }
        },
        error: function () {
            // Handle errors if any
            alert('Error submitting form');
        }
        });
    })
});