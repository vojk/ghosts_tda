let usernames

$(function () { //odstranění uzivatele pomocí ajax protokolu
    $('#form-delete').submit(function (event) {
        console.log(itemId)
        event.preventDefault()
        $.ajax({
            type: "POST",
            url: "/user/" + itemId + "/delete/",
            success: function (response) {
                document.getElementById('_remove_approval').style.display = 'none'
                get_user_table('/app/appUpt/updateUserList');
            },
        });
    });
});



$(function () {
    $('#button-add-user').click(function () {
        $.get('/user/add', function (data) {
            console.log(data)
            $('#_addEdit_window').html(data);
        })
    });
})

function getUsername(username) {
    usernames = username
    console.log(username)
}

$(function () {
    $('#button_edit_user').click(function () {
        console.log(usernames)
        $.get('/user/' + usernames + '/edit/', function (data) {
            console.log(data)
            $('#_addEdit_window').html(data);
        })
    });
})


function get_user_table(url) {
    $.get(url, function (data) {
        console.log(data)
        $('#table').html(data);
    })
}