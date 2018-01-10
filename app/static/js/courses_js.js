//function that calls multiple functions onload
function initialize() {
    createCourseButtons("CSc 100");
    createDiv("CSc 100");
    createCourseButtons("CSc 101");
}

//creates a button for every enrolled course in the database 
function createCourseButtons(str) {
    var courseButton = document.createElement("BUTTON");
    var text = document.createTextNode(str);
    courseButton.appendChild(text);
    //courseButton.addEventListener("click", changeDivContent(str));
    document.getElementById("courses").appendChild(courseButton);
}

function createDiv(str) {
    var div = document.createElement("DIV");
    var txt = document.createTextNode(str);
    div.appendChild(txt);
    div.setAttribute('id', str);
    //div.setAttribute('style', )
    document.getElementById("data").appendChild(div);
}

function changeDivContent(str) {
    var text = document.createTextNode(str);
    document.getElementById(str).appendChild();
}

