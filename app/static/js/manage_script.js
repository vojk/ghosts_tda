$(function () {
    $('#Submit').on('click', function (event) {

    })

    $('#form_note').on('submit', function (event) {
        event.preventDefault();
        var id = $(this).attr('id_note');
        var formData = $(this).serialize();
        console.log(formData);
        $.ajax({
            type: "POST",
            url: "/note/manage/" + id + "/edit/",
            data: formData,
            success: function (response) {
                console.log(response);
                // Other code to handle the server response
            }
        });
    });

    $('#Delete').on('click', function (event) {
        id = $(this).parent().attr('id_note')
        $.ajax({
            type: "POST",
            url: "/note/manage/" + id + "/remove",
            response: function (response) {
                console.log(response)
            }
        })
    })
})