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
    contextMenu.css("display", "none");
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
        contextMenu.css('display', 'none')
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
        contextMenu.css('display', 'none')
    })
}

function showUsers() {
    $.get('/app/user/', function (data) {
        $('#_addEdit_window').html(data);
        contextMenu.css('display', 'none')
    })
}
