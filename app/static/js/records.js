function get_record_id(record) {
    record_id = record
    console.log(record)
}

$(function () {
    table_contextMenu()
})

function hide_clickable_element_via_id(element_id) {
    if (element_id !== "contextMenu_record_more_section") {
        if (contextMenu !== "") {
            contextMenu.hide();
        }
    }

    if (element_id !== "backup_menu") {
        if ($('#backup_menu') !== "") {
            $('#backup_menu').hide()
        }
    }

    if (element_id !== "cont_filt_manu") {
        if ($('.cont_filt_manu') !== "") {
            $('.cont_filt_manu').hide()
        }
    }

    if (element_id !== "menuUser") {
        if ($('.menuUser') !== "") {
            $('.menuUser').hide()
        }
    }


}

$(document).click(function (event) {
    hide_clickable_element_via_id("")
});

function table_contextMenu() {
    $('.contextMenu_record_more_section').on("click", function (event) {
        hide_clickable_element_via_id('contextMenu_record_more_section')
        $('.contextMenu_record').css("display", "none")
        contextMenu = $(this).parent().find('.contextMenu_record')
        console.log(contextMenu.css('display'))
        if (contextMenu.css('display') === "none") {
            contextMenu.css('display', 'flex')
            event.stopPropagation();
        } else {
            contextMenu.css('display', 'none')
        }
    })

    $('.contextMenu_record').on("click", function (event) {
        event.stopPropagation();
    });
}

function remove_record() {
    $.get('/app/' + record_id + '/delete/', function (data) {
        $('#_addEdit_window').html(data);
        deleteModal("", 'Přeješ si smazat tento záznam?');
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }
        animate_filters()
    })
}

function add_record() {
    $.get('/app/add/', function (data) {
        $('#_addEdit_window').html(data);
    })
    animate_filters()
}

function edit_record() {
    $.get('/app/' + record_id + '/edit/', function (data) {
        $('#_addEdit_window').html(data);
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }
        animate_filters()
    })
}

function showUsers() {
    $.get('/app/user/', function (data) {
        $('#_addEdit_window').html(data);
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }
        animate_filters()
    })
}


function showRecord(id) {
    $.get('/app/overview/' + id, function (data) {
        $('#_addEdit_window').html(data);
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }
        animate_filters()
    })
}

function showCategories() {
    $.get('/app/categories/', function (data) {
        $('#_addEdit_window').html(data);
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }
        animate_filters()
    })
}

function animate_filters() {


    $({deg: currentDeg}).animate({deg: 0}, {
        duration: 250,
        step: function (now) {
            $('.arrow_filters').css({
                transform: 'rotate(' + now + 'deg)'
            })
            currentDeg = now
        }
    })
    $({pos: currentPos}).animate({pos: 10}, {
        duration: 250,
        step: function (pos) {
            $('.button_filters_wrap').css({
                right: pos + 'px'
            })
            currentPos = pos
        }
    })
    $({posF: currentPosF}).animate({posF: -375}, {
        duration: 250,
        step: function (posF) {
            $('.main_filter_section_wrapper').css({
                right: posF + 'px'
            })
            currentPosF = posF
        }
    })
}

$(function () {
    $('#backup_upload').on('change', function (e) {
        var csvData
        // Get the selected file
        var file = e.target.files[0];

        // Create a new FileReader instance
        var reader = new FileReader();

        // Set a callback function to run when file is loaded
        reader.onload = function (event) {
            // Parse the CSV data using jQuery CSV plugin
            csvData = $.csv.toArrays(event.target.result);
            var jsonData = [];
            var headers = csvData[0];
            for (var i = 1; i < csvData.length; i++) {
                var obj = {};
                for (var j = 0; j < headers.length; j++) {
                    obj[headers[j]] = csvData[i][j];
                }
                jsonData.push(obj);
            }

            console.log(jsonData)

            $.ajax({
                type: "POST",
                url: "/csv/import",
                data: JSON.stringify(jsonData),
                contentType: 'application/json',
                success: function (response) {
                    sortWithoutRefresh()
                }
            })
        };

        // Read the file as text
        reader.readAsText(file);
    })

    $('.arrow_filters_button').on("click", function () {
        if (currentDeg <= 1) {
            $({deg: currentDeg}).animate({deg: 180}, {
                duration: 250,
                step: function (now) {
                    $('.arrow_filters').css({
                        transform: 'rotate(' + now + 'deg)'
                    })
                    currentDeg = now
                }
            })
            $({pos: currentPos}).animate({pos: 380}, {
                duration: 250,
                step: function (pos) {
                    $('.button_filters_wrap').css({
                        right: pos + 'px'
                    })
                    currentPos = pos
                }
            })

            $({posF: currentPosF}).animate({posF: 0}, {
                duration: 250,
                step: function (posF) {
                    $('.main_filter_section_wrapper').css({
                        right: posF + 'px'
                    })
                    currentPosF = posF
                }
            })

        } else {
            animate_filters()
        }


        console.log(currentDeg)
    })

    $('#backup_button').on('click', function (event) {
        event.stopPropagation();
        hide_clickable_element_via_id('backup_menu')
        if ($('#backup_menu').css('display') === 'flex') {
            $('#backup_menu').css('display', 'none')
        } else {
            $('#backup_menu').css('display', 'flex')
        }
    })

    $('#filters_button').on('click', function (event) {
        event.stopPropagation();
        hide_clickable_element_via_id('cont_filt_manu')
        if ($('.cont_filt_manu').css('display') === 'flex') {
            $('.cont_filt_manu').css('display', 'none')
        } else {
            $('.cont_filt_manu').css('display', 'flex')
        }
    })

    $('.cont_filt_manu').on('click', function (event) {
        event.stopPropagation();
    })

    $('#logout_user').on('click', function () {
        $.get('/app/logout', function () {
            console.log("Logged out")
            location.reload()
        })
    })

    $('#show_user_info').on('click', function (event) {
        event.stopPropagation();
        hide_clickable_element_via_id('menuUser')
        if ($('.menuUser').css('display') === 'flex') {
            $('.menuUser').css('display', 'none')
        } else {
            $('.menuUser').css('display', 'flex')
        }
    })
})

function csv_download() {
    $.ajax({
        url: '/csv/export',
        type: 'GET',
        success: function (data) {
            console.log(data.csv_data)
            var dt = new Date();
            dt.setMonth(dt.getMonth() + 1)
            var time = dt.getHours() + "-" + dt.getMinutes() + "_" + dt.getDate() + "-" + dt.getMonth() + "-" + dt.getFullYear();
            var csvData = 'data:text/csv;charset=utf-8,' + encodeURIComponent(data.csv_data);
            var link = document.createElement('a');
            link.setAttribute('href', csvData);
            link.setAttribute('download', time + '-' + 'backup.csv');
            document.body.appendChild(link);
            link.click();
            link.remove()
        },
        error: function (error) {
            console.log(error);
        }
    });
}

$('html').on("click", function () {
    $('#_addEdit_window').css('display', 'none')
    $('#addWindow').remove()
})
