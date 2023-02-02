date = document.forms["addRecord"]["formDate"];
time = document.forms["addRecord"]["formMinutes"];
desc = document.forms["addRecord"]["formDesc"];
programmer = document.forms["addRecord"]["formProgrammer_select"];
progLang = document.forms["addRecord"]["formProgLang_select"];

function validateForm() {
    if (date.value == "" && !(date.classList.contains('invalid'))) {
        date.classList.add('invalid')
    } else if (!(date.value == "")) {
        date.classList.remove('invalid')
    }

    if (time.value == "" && !(time.classList.contains('invalid')) || time.value == "0" && !(time.classList.contains('invalid'))) {
        time.classList.add('invalid')
    } else if (!(time.value == "")) {
        time.classList.remove('invalid')
    }

    if (progLang.value == "None" && !(progLang.classList.contains('invalid'))) {
        progLang.classList.add('invalid')
    } else if (!(progLang.value == "None")) {
        progLang.classList.remove('invalid')
    }

    if (desc.value == "" && !(desc.classList.contains('invalid'))) {
        desc.classList.add('invalid')
    } else if (!(desc.value == "")) {
        desc.classList.remove('invalid')
    }

    if (programmer.value == "None" && !(programmer.classList.contains('invalid'))) {
        programmer.classList.add('invalid')
    } else if (!(programmer.value == "None")) {
        programmer.classList.remove('invalid')
    }

    if (date.value === "" || time.value === "" || time.value === "0" || desc.value === "" || programmer.value === "None") {
        return false;
        canBePosted = false
    } else{
        canBePosted = true
    }
}

date.addEventListener('input', function (evt) {
    if (this.value !== "") {
        this.classList.remove('invalid')
    }
});

time.addEventListener('input', function (evt) {
    if (this.value !== "") {
        this.classList.remove('invalid')
    }
});

desc.addEventListener('input', function (evt) {
    if (this.value !== "") {
        this.classList.remove('invalid')
    }
});

$('#_formMinutes').on('keypress', function (e) {
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