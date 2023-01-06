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

$(function () {
    $('#filter-form').submit(function (event) {
        event.preventDefault();
        var filterMinDate = $('#filter_min_date').val();
        var filterMaxDate = $('#filter_max_date').val();
        var filterMinRating = $('#min-value').val();
        var filterMaxRating = $('#max-value').val();
        var filterprogramingLangs = $('#filter_programmingLangs').val();
        var sortField = $('#sort_field').val();
        var sortParameter = $('#sort_order').val();
        var filterprogramingLangsFormated = "";
        var dateFormated = filterMinDate + "," + filterMaxDate
        var filterRating = filterMinRating + "," + filterMaxRating
        for (const element of filterprogramingLangs) {
            filterprogramingLangsFormated += element + ","
        }

        filterprogramingLangsFormated = filterprogramingLangsFormated.slice(0, -1)
        console.log(filterprogramingLangsFormated)

        $.get('/sort', {
            sort_field: sortField,
            sort_parameter: sortParameter,
            filter_rating: filterRating,
            filter_programmingLangs: filterprogramingLangsFormated,
            filter_formatted_date: dateFormated
        }, function (data) {
            // data is the HTML of the updated table
            $('#table').html(data);
        });
    });
});


$(function () {
        document.getElementById('filter_max_date').valueAsDate = new Date()
    }
)

