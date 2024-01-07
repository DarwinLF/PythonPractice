$(document).ready(function(){
    $('#createBookModal').on('shown.bs.modal', function () {
        $('#authorBookButton').hide();
        $('#libraryBookButton').hide();
    });

    $('#createCustomerModal').on('shown.bs.modal', function () {
        $('#libraryCustomerButton').hide();
    });

    $('#createEmployeeModal').on('shown.bs.modal', function () {
        $('#libraryEmployeeButton').hide();
    });
});