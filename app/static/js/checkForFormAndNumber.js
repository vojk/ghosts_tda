date = $('#_formDate')
time = $('#_formMinutes')
desc = $('#_formDesc')
progLang = $('#_formProgLang_select')

function validateForm() {
    if (date.val() === "" && !(date.hasClass('invalid'))) {
        date.addClass('invalid')
    } else if (!(date.val() === "")) {
        date.removeClass('invalid')
    }

    if (time.val() === "" || (time.val() === "0" && !(time.hasClass('invalid')))) {
        time.addClass('invalid');
        time.parent().parent().find('.w_selector').css('opacity', '1')
    } else if (time.val() !== "" && time.val() !== "0") {
        time.removeClass('invalid');
        time.parent().parent().find('.w_selector').css('opacity', '0')
    }

    if (progLang.val() === "None" && !(progLang.hasClass('invalid'))) {
        progLang.addClass('invalid')
        progLang.parent().parent().find('.w_selector').css('opacity', '1')
    } else if (!(progLang.val() == "None")) {
        progLang.removeClass('invalid')
        progLang.parent().parent().find('.w_selector').css('opacity', '0')
    }

    if (desc.val() === "" && !(desc.hasClass('invalid'))) {
        desc.addClass('invalid')
        desc.parent().parent().find('.w_selector').css('opacity', '1')
    } else if (!(desc.val() === "")) {
        desc.removeClass('invalid')
        desc.parent().parent().find('.w_selector').css('opacity', '0')
    }

    console.log((time.val() === "" || time.val() === "0"))

    if (date.val() === "" || (time.val() === "" || time.val() === "0") || desc.val() === "") {
        canBePosted = false
        return false;
    } else {
        canBePosted = true
    }
}

$(date).on('input', function () {
    if ($(this).val() !== "") {
        $(this).removeClass('invalid')
    } else {
        $(this).addClass('invalid')
        $(this).parent().parent().find('.w_selector').css('opacity', '1')
    }
})

$(time).on('input', function () {
    if ($(this).val() !== "" && time.val() !== "0") {
        $(this).removeClass('invalid')
        $(this).parent().parent().find('.w_selector').css('opacity', '0')
    } else {
        $(this).addClass('invalid')
        $(this).parent().parent().find('.w_selector').css('opacity', '1')
    }
})

$(desc).on('input', function () {
    if ($(this).val() !== "") {
        $(this).removeClass('invalid')
        $(this).parent().parent().find('.w_selector').css('opacity', '0')
    } else {
        $(this).addClass('invalid')
        $(this).parent().parent().find('.w_selector').css('opacity', '1')
    }
})

$(progLang).on('change', function () {
    if ($(this).val() !== "None") {
        $(this).removeClass('invalid')
        $(this).parent().parent().find('.w_selector').css('opacity', '0')
    } else {
        $(this).addClass('invalid')
        $(this).parent().parent().find('.w_selector').css('opacity', '1')
    }
})

time.on('keypress', function (e) {
    return e.metaKey || // cmd/ctrl
        e.which <= 0 || // arrow keys
        e.which == 8 || // delete key
        /[0-9]/.test(String.fromCharCode(e.which)); // numbers
})


$("[id$=sharp]").each(function () {
    var text = $(this).text();

    text = text.replace('sharp', '#');
    $(this).text(text);
})