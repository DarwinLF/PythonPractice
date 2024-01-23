function attachEmployeeSubmitHandler() {
    $('#employee_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: '/persons/employee/createEmployee/modal/',
        data: $(this).serialize(),
        success: function(response) {
            if(response.status === 'success') {
                $('#createEmployeeModal').modal('hide');
                $('#employee_form')[0].reset();
                location.reload();
            }
            else {
                $('#employeeBodyModal').html(response.errors)
                $('#libraryEmployeeButton').hide();
                attachEmployeeSubmitHandler();
            }
        },
        error: function (error) {
            // Handle errors if any
            if (error.responseJSON && error.responseJSON.status === 'error') {
                // Update the form with errors
                $('#employeeBodyModal').html(error.responseJSON.errors);
                attachEmployeeSubmitHandler();
            }
        }
        });
    })
}

$(document).ready(function(){
    attachEmployeeSubmitHandler();
});