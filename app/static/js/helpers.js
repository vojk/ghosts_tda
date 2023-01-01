function setSameRecord() {
    let date = document.forms["addRecord"]["formDate"];
    let time = document.forms["addRecord"]["formMinutes"];
    let desc = document.forms["addRecord"]["formDesc"];
    let progLang = document.forms["addRecord"]["formProgLang_select"];
    let progLangItems = progLang.getElementsByTagName('option');
    let rating = document.forms["addRecord"]["formRating"];

    let index = Math.floor(Math.random() * progLangItems.length) + 1

    while (index >= progLangItems.length) {
        index = Math.floor(Math.random() * progLangItems.length) + 1
    }

    date.valueAsDate = new Date(Math.floor(Math.random() * 13) + 2009, Math.floor(Math.random() * 12) + 1, Math.floor(Math.random() * 28) + 1)
    time.value = Math.floor(Math.random() * 151)+1
    desc.value = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab ad alias consequuntur corporis culpa earum esse est ex explicabo incidunt iusto labore laborum laudantium minima molestias quam, quibusdam recusandae ullam?'
    progLang.selectedIndex = index
    rating.value = Math.floor(Math.random() * 6)

    let jsonString = '{"date": " ' + date.value + '", "time": " ' + time.value + '", "progLang": " ' + progLang.value + '", "rating": " ' + rating.value + '", "desc": " ' + desc.value + '"}';
    let jsonPretty = JSON.stringify(JSON.parse(jsonString), null, 2);

    console.log(jsonPretty)
}