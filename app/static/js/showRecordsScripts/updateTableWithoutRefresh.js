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
var filterProgrammer
var filterCategories

var sort_programmer_statement = ""
var sort_programLang_statement = ""
var sort_time_statement = ""
var sort_dates_statement = ""
var sort_rating_statement = ""

let sort_temp_complete_statement = [];
let sort_element_to_remove = ""

let filter_programmingLangs = [];
let filter_categories = [];

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

$(function () {
    $('#filter_programmingLangs option').on('click', function () {
        console.log(this.value)
        const index = filter_programmingLangs.findIndex(element => {
            if (element.includes(this.value)) {
                return true;
            }
        });
        var ids = this.id
        ids = ids.replace(" option", "")
        console.log(ids)

        if (index !== -1) {
            filter_programmingLangs.splice(index, 1)
        } else {
            if (this.value !== "None") {
                filter_programmingLangs.push(this.value)
                $('#' + ids).css("background-color", "green")
            } else {
                filter_programmingLangs = []
            }
        }

        if (filter_programmingLangs)
            console.log(filter_programmingLangs)
    })
})

//sortování
$(function () {
    $('#sort-button-programmer').click(function () {
        if (sort_programmer_statement === "") {
            sort_programmer_statement = "programmer ASC"
            $('#sort-button-programmer-az').css("opacity", "0")
            $('#sort-button-programmer-za').css("opacity", "1")
        } else if (sort_programmer_statement === "programmer ASC") {
            sort_programmer_statement = "programmer DESC"
            $('#sort-button-programmer-az').css("opacity", "1")
            $('#sort-button-programmer-za').css("opacity", "0")
        } else {
            sort_programmer_statement = ""
            $('#sort-button-programmer-az').css("opacity", "1")
            $('#sort-button-programmer-za').css("opacity", "1")
            sort_element_to_remove = "programmer DESC"
        }
        console.log(sort_programmer_statement)
        appendListOfSort(sort_programmer_statement)
        sortWithoutRefresh()
    });
});

$(function () {
    $('#sort-button-programLang').click(function () {
        if (sort_programLang_statement === "") {
            sort_programLang_statement = "programmingLang ASC"
            $('#sort-button-programmingLang-az').css("opacity", "0")
            $('#sort-button-programmingLang-za').css("opacity", "1")
        } else if (sort_programLang_statement === "programmingLang ASC") {
            sort_programLang_statement = "programmingLang DESC"
            $('#sort-button-programmingLang-az').css("opacity", "1")
            $('#sort-button-programmingLang-za').css("opacity", "0")
        } else {
            sort_programLang_statement = ""
            $('#sort-button-programmingLang-az').css("opacity", "1")
            $('#sort-button-programmingLang-za').css("opacity", "1")
            sort_element_to_remove = "programmingLang DESC"
        }
        console.log(sort_programLang_statement)
        appendListOfSort(sort_programLang_statement)
        sortWithoutRefresh()
    });
});

$(function () {
    $('#sort-button-time').click(function () {
        if (sort_time_statement === "") {
            sort_time_statement = "timeInMinutes ASC"
            $('#sort-button-timeInMinutes-az').css("opacity", "0")
            $('#sort-button-timeInMinutes-za').css("opacity", "1")
        } else if (sort_time_statement === "timeInMinutes ASC") {
            sort_time_statement = "timeInMinutes DESC"
            $('#sort-button-timeInMinutes-az').css("opacity", "1")
            $('#sort-button-timeInMinutes-za').css("opacity", "0")
        } else {
            sort_time_statement = ""
            $('#sort-button-timeInMinutes-az').css("opacity", "1")
            $('#sort-button-timeInMinutes-za').css("opacity", "1")
            sort_element_to_remove = "timeInMinutes DESC"
        }
        console.log(sort_time_statement)
        appendListOfSort(sort_time_statement)
        sortWithoutRefresh()
    });
});


$(function () {
    $('#sort-button-date').click(function () {
        if (sort_dates_statement === "") {
            sort_dates_statement = "dates ASC"
            $('#sort-button-dates-az').css("opacity", "0")
            $('#sort-button-dates-za').css("opacity", "1")
        } else if (sort_dates_statement === "dates ASC") {
            sort_dates_statement = "dates DESC"
            $('#sort-button-dates-az').css("opacity", "1")
            $('#sort-button-dates-za').css("opacity", "0")
        } else {
            sort_dates_statement = ""
            $('#sort-button-dates-az').css("opacity", "1")
            $('#sort-button-dates-za').css("opacity", "1")
            sort_element_to_remove = "dates DESC"
        }
        console.log(sort_dates_statement)
        appendListOfSort(sort_dates_statement)
        sortWithoutRefresh()
    });
});

$(function () {
    $('#sort-button-rating').click(function () {
        if (sort_rating_statement === "") {
            sort_rating_statement = "rating ASC"
            $('#sort-button-rating-az').css("opacity", "0")
            $('#sort-button-rating-za').css("opacity", "1")
        } else if (sort_rating_statement === "rating ASC") {
            sort_rating_statement = "rating DESC"
            $('#sort-button-rating-az').css("opacity", "1")
            $('#sort-button-rating-za').css("opacity", "0")
        } else {
            sort_rating_statement = ""
            $('#sort-button-rating-az').css("opacity", "1")
            $('#sort-button-rating-za').css("opacity", "1")
            sort_element_to_remove = "rating DESC"
        }
        console.log(sort_rating_statement)
        appendListOfSort(sort_rating_statement)
        sortWithoutRefresh()
    });
});

let prevElement = ""

function appendListOfSort(newElement) {
    let testNewElement

    if (newElement.includes("ASC")) {
        testNewElement = newElement.replace(" ASC", "")
    } else if (newElement.includes("DESC")) {
        testNewElement = newElement.replace(" DESC", "")
    }

    console.log(testNewElement)

    if (!(prevElement.includes(testNewElement)) && prevElement !== "") {
        sort_temp_complete_statement = []

        var prevElement_temp

        if (prevElement.includes("ASC")) {
            prevElement_temp = prevElement.replace(" ASC", "")
        } else if (prevElement.includes("DESC")) {
            prevElement_temp = prevElement.replace(" DESC", "")
        }

        $('#sort-button-' + prevElement_temp + '-az').css("opacity", "1")
        $('#sort-button-' + prevElement_temp + '-za').css("opacity", "1")

        switch (prevElement_temp) {
            case 'programmer':
                sort_programmer_statement = ""
                break;
            case 'programmingLang':
                sort_programLang_statement = ""
                break;
            case 'timeInMinutes':
                sort_time_statement = ""
                break;
            case 'dates':
                sort_dates_statement = ""
                break;
            case 'rating':
                sort_rating_statement = ""
                break;
        }
    }

    const index = sort_temp_complete_statement.findIndex(element => {
        if (element.includes(testNewElement)) {
            return true;
        }
    });

    if (index !== -1) {
        sort_temp_complete_statement.splice(index, 1)
        console.log("There you go " + sort_temp_complete_statement[index])
        if (newElement !== "") {
            sort_temp_complete_statement.push(newElement)
        }
    } else {
        if (newElement !== "") {
            sort_temp_complete_statement.push(newElement)
        } else {
            const indexOld = sort_temp_complete_statement.findIndex(element => {
                if (element.includes(sort_element_to_remove)) {
                    return true;
                }
            });
            sort_temp_complete_statement.splice(indexOld, 1)
        }
    }

    sortParameterFormatted = sort_temp_complete_statement[0]

    prevElement = newElement

    console.log(sort_temp_complete_statement)

    console.log(index);
}

//function appendListOfSort(newElement) {
//    let testNewElement
//
//    console.log(newElement)
//    if (newElement.includes("ASC")) {
//        testNewElement = newElement.replace(" ASC", "")
//    } else if (newElement.includes("DESC")) {
//        testNewElement = newElement.replace(" DESC", "")
//    }
//
//    const index = sort_temp_complete_statement.findIndex(element => {
//        if (element.includes(testNewElement)) {
//            return true;
//        }
//    });
//
//    console.log(index);
//
//    if (index !== -1) {
//        sort_temp_complete_statement.splice(index, 1)
//        console.log("There you go " + sort_temp_complete_statement[index])
//        if (newElement !== "") {
//            sort_temp_complete_statement.push(newElement)
//        }
//    } else {
//        if (newElement !== "") {
//            sort_temp_complete_statement.push(newElement)
//        } else {
//            const indexOld = sort_temp_complete_statement.findIndex(element => {
//                if (element.includes(testNewElement)) {
//                    return true;
//                }
//            });
//            if (newElement === prevElement) {
//                sort_temp_complete_statement.splice(indexOld, 1)
//            }
//            if (sort_element_to_remove !== "") {
//                const index_to_remove = sort_temp_complete_statement.findIndex(element => {
//                    if (element.includes(sort_element_to_remove)) {
//                        return true;
//                    }
//                });
//                sort_temp_complete_statement.splice(index_to_remove, 1)
//            }
//        }
//    }
//
//    prevElement = newElement
//
//    sortParameterFormatted = ""
//
//    for (const element of sort_temp_complete_statement) {
//        sortParameterFormatted += element + ","
//    }
//    sortParameterFormatted = sortParameterFormatted.slice(0, -1)
//
//    console.log(sortParameterFormatted)
//    console.log("your old element: " + prevElement)
//    console.log(sort_temp_complete_statement)
//
//    //sortParameterFormatted
//}

$(function () { //odstranění záznamu pomocí ajax protokolu
    $('#form-delete').submit(function (event) {
        event.preventDefault()
        $.ajax({
            type: "POST", url: "/app/" + itemId + "/delete/", success: function (response) {
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
        filter_time: filterTime,
        filter_programmer: filterProgrammer,
        filter_categories: filterCategories
    }, function (data) {
        // data is the HTML of the updated table
        $('#table-content').html(data);
    });
}


function getValues() { //získání hodnot ze selectorů
    filterMinDate = $('#filter_min_date').val();
    filterMaxDate = $('#filter_max_date').val();
    filterMinRating = $('#min_rating').val();
    filterMaxRating = $('#max_rating').val();
    filterMinTime = $('#min_time').val();
    filterMaxTime = $('#max_time').val();
    //filterprogramingLangs = $('#filter_programmingLangs').val();
    sortField = $('#sort_field').val();
    sortParameter = $('#sort_order').val();
    filterProgrammer = $('#filter_programmers').val();
    filterprogramingLangsFormated = "";
    filterCategories = "";
    dateFormated = filterMinDate + "," + filterMaxDate
    filterRating = filterMinRating + "," + filterMaxRating
    filterTime = filterMinTime + "," + filterMaxTime
    //sortParameterFormatted = sortField + " " + sortParameter
    for (const element of filter_programmingLangs) {
        filterprogramingLangsFormated += element + ","
    }

    for (const element of filter_categories) {
        filterCategories += element + ","
    }
    filterprogramingLangsFormated = filterprogramingLangsFormated.slice(0, -1)
    filterCategories = filterCategories.slice(0, -1)

    console.log(filterCategories)
}

$(function () {
    document.getElementById('filter_max_date').valueAsDate = new Date()
})

