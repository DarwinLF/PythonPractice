$(document).ready(function(){
    var bookSelect = $('#bookSelect');
    bookSelect.empty();
    bookSelect.append('<option value="" selected="">---------</option>')

    var customerSelect = $('#customerSelect');
    customerSelect.empty();
    customerSelect.append('<option value="" selected="">---------</option>')

    var employeeSelect = $('#employeeSelect');
    employeeSelect.empty();
    employeeSelect.append('<option value="" selected="">---------</option>')

    $('#librarySelect').on('change', function() {
        var selectedLibrary = $(this).val();
        $.ajax({
            url: '/libraries/rent/ajax/getLibrary/' + selectedLibrary,
            success: function(data){
                var books = JSON.parse(data.books)
                var bookSelect = $('#bookSelect');
                bookSelect.empty();
                bookSelect.append('<option value="" selected="">---------</option>')
                $.each(books, function(index, book){
                    bookSelect.append('<option value="' + book.pk + '">' + book.fields.title + '</option>');
                });

                var customers = JSON.parse(data.customers)
                var customerSelect = $('#customerSelect');
                customerSelect.empty();
                customerSelect.append('<option value="" selected="">---------</option>')
                $.each(customers, function(index, customer){
                    customerSelect.append('<option value="' + customer.pk + '">' + customer.fields.first_name + ' ' + customer.fields.last_name + '</option>');
                });

                var employees = JSON.parse(data.employees)
                var employeeSelect = $('#employeeSelect');
                employeeSelect.empty();
                employeeSelect.append('<option value="" selected="">---------</option>')
                $.each(employees, function(index, employees){
                    employeeSelect.append('<option value="' + employees.pk + '">' + employees.fields.first_name + ' ' + employees.fields.last_name + '</option>');
                });
            }
        });
    });
});