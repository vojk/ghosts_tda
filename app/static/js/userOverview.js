let usernames
let _statement

var legend_text


function getUsername(username) {
    usernames = username
    console.log(username)
}

$(function () {
    $('#button-add-user').click(function () {
        $.get('/user/add', function (data) {
            $('#_addEdit_window').html(data);
            get_addEdit_statement('button-add-user')
        })
    });
})

$(function () {
    $('#button_delete_user').click(function () {
        $.get('/user/delete/', function (data) {
            $('#_addEdit_window').html(data);
            set_remove_statement('user')
        })
    });
})


function edit_user() {
    console.log(usernames)
    $.get('/user/' + usernames + '/edit/', function (data) {
        $('#_addEdit_window').html(data);
        get_addEdit_statement('button_edit_user')
    })
}

function remove_user() {
    $.get('/user/' + usernames + '/delete/', function (data) {
        $('#_addEdit_window').html(data);
        deleteModal(usernames, 'Přeješ si smazat uživatele ' + usernames + '?');
    })
}

function get_user_table(url) {
    $.get(url, function (data) {
        $('#table').html(data);
    })
}