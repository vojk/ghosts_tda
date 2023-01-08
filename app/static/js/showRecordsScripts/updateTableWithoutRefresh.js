$(function () {
    $('#sort-form').submit(function (event) {
        event.preventDefault();
        shortDesc()
        var filterMinDate = $('#filter_min_date').val();
        var filterMaxDate = $('#filter_max_date').val();
        var filterMinRating = $('#min_rating').val();
        var filterMaxRating = $('#max_rating').val();
        var filterMinTime = $('#min_time').val();
        var filterMaxTime = $('#max_time').val();
        var filterprogramingLangs = $('#filter_programmingLangs').val();
        var sortField = $('#sort_field').val();
        var sortParameter = $('#sort_order').val();
        var filterprogramingLangsFormated = "";
        var dateFormated = filterMinDate + "," + filterMaxDate
        var filterRating = filterMinRating + "," + filterMaxRating
        var filterTime = filterMinTime + "," + filterMaxTime
        var sortParameterFormatted = sortField + " " + sortParameter
        for (const element of filterprogramingLangs) {
            filterprogramingLangsFormated += element + ","
        }

        filterprogramingLangsFormated = filterprogramingLangsFormated.slice(0, -1)

        $.get('/sort', {
            sort_field: sortParameterFormatted,
            sort_parameter: sortParameter,
            filter_rating: filterRating,
            filter_programmingLangs: filterprogramingLangsFormated,
            filter_formatted_date: dateFormated,
            filter_time: filterTime
        }, function (data) {
            // data is the HTML of the updated table
            $('#table').html(data);
        });
    });
});

$(function () {
    $('#filter-form').submit(function (event) {
        event.preventDefault();
        shortDesc()
        var filterMinDate = $('#filter_min_date').val();
        var filterMaxDate = $('#filter_max_date').val();
        var filterMinRating = $('#min_rating').val();
        var filterMaxRating = $('#max_rating').val();
        var filterMinTime = $('#min_time').val();
        var filterMaxTime = $('#max_time').val();
        var filterprogramingLangs = $('#filter_programmingLangs').val();
        var sortField = $('#sort_field').val();
        var sortParameter = $('#sort_order').val();
        var filterprogramingLangsFormated = "";
        var dateFormated = filterMinDate + "," + filterMaxDate
        var filterRating = filterMinRating + "," + filterMaxRating
        var filterTime = filterMinTime + "," + filterMaxTime
        var sortParameterFormatted = sortField + " " + sortParameter
        for (const element of filterprogramingLangs.split(",")) {
            filterprogramingLangsFormated += element + ","
        }

        filterprogramingLangsFormated = filterprogramingLangsFormated.slice(0, -1)

        $.get('/sort', {
            sort_field: sortParameterFormatted,
            sort_parameter: sortParameter,
            filter_rating: filterRating,
            filter_programmingLangs: filterprogramingLangsFormated,
            filter_formatted_date: dateFormated,
            filter_time: filterTime
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

