var filterMinDate
var filterMaxDate
var filterMinRating
var filterMaxRating
var filterMinTime
var filterMaxTime
var filterprogramingLangs
var sortField
var sortParameter
var filterprogramingLangsFormated = "";
var dateFormated
var filterRating
var filterTime
var sortParameterFormatted

var itemId

$(function () { //sort form získání a zobrazení dat
    $('#sort-form').submit(function (event) {
        event.preventDefault();
        shortDesc()
        getValues()

        sortWithoutRefresh()
    });
});

$(function () { //filter form získání a zobrazení dat
    $('#filter-form').submit(function (event) {
        event.preventDefault();
        shortDesc()
        getValues()

        console.log(filterprogramingLangs)

        sortWithoutRefresh()
    });
});

function deleteModal(id) { //Získání id postu + zobrazení delete formu
    itemId = id
    document.getElementById('_remove_approval').style.display = 'block'
}

$(function () { //odstranění záznamu pomocí ajax protokolu
    $('#form-delete').submit(function (event) {
        event.preventDefault()
        $.ajax({
            type: "POST",
            url: "/app/" + itemId + "/delete/",
            success: function (response) {
                sortWithoutRefresh()
                document.getElementById('_remove_approval').style.display = 'none'
            },
        });
    });
});

function sortWithoutRefresh() { //funkce pro sort
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
}

function getValues() { //získání hodnot ze selectorů
    filterMinDate = $('#filter_min_date').val();
    filterMaxDate = $('#filter_max_date').val();
    filterMinRating = $('#min_rating').val();
    filterMaxRating = $('#max_rating').val();
    filterMinTime = $('#min_time').val();
    filterMaxTime = $('#max_time').val();
    filterprogramingLangs = $('#filter_programmingLangs').val();
    sortField = $('#sort_field').val();
    sortParameter = $('#sort_order').val();
    filterprogramingLangsFormated = "";
    dateFormated = filterMinDate + "," + filterMaxDate
    filterRating = filterMinRating + "," + filterMaxRating
    filterTime = filterMinTime + "," + filterMaxTime
    sortParameterFormatted = sortField + " " + sortParameter
    for (const element of filterprogramingLangs.split(",")) {
        filterprogramingLangsFormated += element + ","
    }

    filterprogramingLangsFormated = filterprogramingLangsFormated.slice(0, -1)
}

$(function () {
    document.getElementById('filter_max_date').valueAsDate = new Date()
})

