$(function () {
    $('#sort-form').submit(function (event) {
        event.preventDefault();
        var sortField = $('#sort_field').val();
        var sortParameter = $('#sort_order').val();
        $.get('/sort', {sort_field: sortField, sort_parameter: sortParameter}, function (data) {
            // data is the HTML of the updated table
            $('#table').html(data);
        });
    });
});