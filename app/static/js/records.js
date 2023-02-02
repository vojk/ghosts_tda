let record_id
let table = ""

let contextMenu = ""
let prevContextMenu = ""

function get_record_id(record) {
    record_id = record
    console.log(record)
}

$(function () {
    table_contextMenu()
})

$("html").click(function (event) {
    if (contextMenu !== "") {
        contextMenu.css("display", "none");
    }
});

function table_contextMenu() {
    $('.contextMenu_record_more_section').on("click", function (event) {
        $('.contextMenu_record').css("display", "none")
        contextMenu = $(this).parent().find('.contextMenu_record')
        event.stopPropagation();
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
    })
}

function add_record() {
    $.get('/app/add/', function (data) {
        $('#_addEdit_window').html(data);
    })
}

function edit_record() {
    $.get('/app/' + record_id + '/edit/', function (data) {
        $('#_addEdit_window').html(data);
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }
    })
}

function showUsers() {
    $.get('/app/user/', function (data) {
        $('#_addEdit_window').html(data);
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }

    })
}


function showCategories() {
    $.get('/app/categories/', function (data) {
        $('#_addEdit_window').html(data);
        if (contextMenu !== "") {
            contextMenu.css('display', 'none')
        }
    })
}

let currentDeg = "0"
let currentPos = "10"
let currentPosF = "-375"
$(function () {
    $('.arrow_filters_button').on("click", function () {
        if (currentDeg <= 0) {
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


        console.log(currentDeg)
    })
})
