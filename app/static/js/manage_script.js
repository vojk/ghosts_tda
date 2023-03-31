$(function () {
    $('#form_note_add').on('submit', function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        console.log(formData);
        $.ajax({
            type: "POST",
            url: "/note/add",
            data: $(this).serialize(),
            success: function (response) {
                console.log(response);
                $('#note_paper_edit').remove()
                $('#edit_window').css('display', 'none')
                $.ajax({
                    type: "GET",
                    url: '/board/',
                    success: function (response) {
                        $('#tenhle_div_je_tu_jen_tak').remove();
                        $('.board').append(response);
                    }
                });
            }
        });
    });

    $('#form_note').on('submit', function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        if (statement === "edit") {
            id = $('note_paper_edit').attr('id_note');
            // Modify the data object to include the ID of the note being edited
            var data = $(this).serializeArray();
            data.push({name: "id", value: id});
            formData = $.param(data);
        }
        console.log(formData);
        $.ajax({
            type: "POST",
            url: "/note/edit",
            data: formData,
            success: function (response) {
                console.log(response);
                $('#note_paper_edit').remove()
                $('#edit_window').css('display', 'none')
                $.ajax({
                    type: "GET",
                    url: '/board/',
                    success: function (response) {
                        $('#tenhle_div_je_tu_jen_tak').remove();
                        $('.board').append(response);
                    }
                });
            }
        });
    });
});
