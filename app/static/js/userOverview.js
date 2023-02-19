let usernames
let user_ids
let _statement

var legend_text

function getUsername(username) {
    usernames = username
    console.log(username)
}

function getUserId(id) {
    user_ids = id
    console.log(user_ids)
}

function addUser_window() {
    $.get('/user/add/', function (data) {
        $('#_addEdit_window_users').html(data);
        get_addEdit_statement('button-add-user')
    })
}

function addUser_window_outOfBox() {
    $.get('/user/add/', function (data) {
        $('#_addEdit_window').html(data);
        $('#_addEdit_window').css('display', 'block')
        $('#user_add-edit_button_cancel').click(function () {
            $('#_addEdit_window').css('display', 'none')
            $('#user_add-edit_window_container').remove()
        })
        $(".outerBox_add-edit_window").click(function (event) {
            $('#_addEdit_window').css('display', 'none')
            $('#user_add-edit_window_container').remove()
        });
        $("#user_add-edit_window_container").click(function (event) {
            event.stopPropagation()
        })
        get_addEdit_statement('button-add-user-out')
    })
}

$(function () {
    $('#button_delete_user').click(function () {
        $.get('/user/delete/', function (data) {
            $('#_addEdit_window_users').html(data);
            set_remove_statement('user')
        })
    });
})


function edit_user() {
    console.log(usernames)
    $.get('/user/' + user_ids + '/edit/', function (data) {
        $('#_addEdit_window_users').html(data);
        get_addEdit_statement('button_edit_user')
    })
}

function remove_user() {
    $.get('/user/' + usernames + '/delete/', function (data) {
        $('#_addEdit_window_users').html(data);
        deleteModal(usernames, 'Přeješ si smazat uživatele ' + usernames + '?');
    })
}

function get_user_table(url) {
    $.get(url, function (data) {
        $('#table_users').html(data);
    })
}