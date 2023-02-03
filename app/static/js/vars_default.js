var self_statement

let canBePosted

let date
let time
let desc
let programmer
let progLang

var form
let colorToSave
let cat_editAddStatement

let id_cat
let prevSelector
var filter_categories = []


var filterMinDate
var filterMaxDate
var filterMinRating
var filterMaxRating
var filterMinTime
var filterMaxTime
var filterprogramingLangs
var sortField
var sortParameter
var filterprogramingLangsFormated = "";
var dateFormated
var filterRating
var filterTime
var sortParameterFormatted
var filterProgrammer
var filterCategories

var sort_programmer_statement = ""
var sort_programLang_statement = ""
var sort_time_statement = ""
var sort_dates_statement = ""
var sort_rating_statement = ""

let sort_temp_complete_statement = [];
let sort_element_to_remove = ""

let filter_programmingLangs = [];

var itemId

var textToBesShorten

//sliders
let rangeMin = 0;
const ranges = document.querySelectorAll(".range");

//records
let record_id
let table = ""

let contextMenu = ""
let prevContextMenu = ""

//animation
let currentDeg = "0"
let currentPos = "10"
let currentPosF = "-375"




let rgb2hex = (rgb) => `#${rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/).slice(1).map(n => parseInt(n, 10).toString(16).padStart(2, '0')).join('')}`

function set_remove_statement(statement) {
    self_statement = statement
    console.log(statement)
}