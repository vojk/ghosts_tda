function setSameRecord() {
    let date = document.forms["addRecord"]["formDate"];
    let time = document.forms["addRecord"]["formMinutes"];
    let desc = document.forms["addRecord"]["formDesc"];
    let progLang = document.forms["addRecord"]["formProgLang_select"];
    let rating = document.forms["addRecord"]["formRating"];

    date.valueAsDate = new Date(2022, 2, 15)
    time.value = '50'
    desc.value = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab ad alias consequuntur corporis culpa earum esse est ex explicabo incidunt iusto labore laborum laudantium minima molestias quam, quibusdam recusandae ullam?'
    progLang.value = 'JAVA'
    rating.value = '3'
}