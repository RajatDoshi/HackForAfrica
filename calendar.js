days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031];

// for(let i = 0; i < 2100; i++){
//     years.push(i);
//     document.createElement("")
// }



console.log(years[2010])
daysInMonth={
    "Jan":31,
    "Feb":28,
    "Mar":31,
    "Apr":30,
    "May":31,
    "Jun":30,
    "Jul":31,
    "Aug":31,
    "Sep":30,
    "Oct":31,
    "Nov":30,
    "Dec":31
}
dayStart={
    "Sun":0,
    "Mon":1,
    "Tue":2,
    "Wed":3,
    "Thu":4,
    "Fri":5,
    "Sat":6
}


let day = new Date()
let month;
let year;
// let tbl = document.querySelector(".Calendar")

console.log(months[day.getMonth()])
console.log(daysInMonth[months[day.getMonth()]])



document.addEventListener("DOMContentLoaded", function(){
    year = years[day.getFullYear()];
    month = months[day.getMonth()];
    document.getElementById("months").selectedIndex = day.getMonth();
    document.getElementById("years")
    let f = new Date();
   buildCalendar(f.getMonth(), f.getFullYear());
})

// alert(`${year} and ${month}`)
// document.getElementById("MyElement").classList.add('MyClass');

document.addEventListener("DOMContentLoaded", function(){

    let t = document.createElement("h1");
    t.innerHTML = "akjsdf";
    document.body.append(t);

})

let tbl = document.querySelector(".Calendar");

function buildCalendar(month, year){
    tbl.innerHTML = " <tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>";

    let m = document.createElement("h1");
    m.innerHTML = months[month];
    document.body.append(m);
    let y = document.createElement("h1");
    y.innerHTML = year;
    document.body.append(y);
    let arr = [];
    let dayR = parseInt(daysInMonth[months[month]])
    // return dayR;
    let nD = new Date(year, month, 1);
    let dayNum = parseInt(nD.getDay());
    // console.log(dayNum);
    let n = 1;
    let dates = 1;
    console.log(dayR)
    for(let i = 0; i < 6; i++){
        let rw  = document.createElement("tr");
        for(let j = 0; j < 7;j++){
            let t = 0
            let index = i*7 + j;
            // let but = document.createElement("button");

            let dat = document.createElement("td");
            let sp = document.createElement("span");
            sp.style.lineHeight = 2;
            if(index < dayNum){
                sp.innerHTML = "";
                rw.appendChild(dat);
                continue;
            }
            if(index < dayR+dayNum){
                sp.innerHTML =  dates;
                dates++;
                // dat.onmouseover = function(){this.style.color = "blue";};
                // dat.onmouseout = function(){this.style.color = "black";};
                sp.classList.add("fal");
                sp.classList.add("hvr-sweep-to-right");

                sp.onclick = function(){ this.classList.toggle("circle");};


            }else{
                sp.innerHTML = "";
            }


            // if(t == 1){
            //     counter++;
                
            // }
            dat.appendChild(sp);
            rw.appendChild(dat);
            
        }
        tbl.appendChild(rw);
    }

}

function hov(object){
    object.classList.add("hov");
}

function dehov(object){
    object.classList.add("dehov");
}
function cli(object){
    object.classList.add("cli");
}
function monthc(){
    let choices = document.getElementById("months");
    let choices1 = document.getElementById("years");
    year = years[choices1.selectedIndex];
    month = choices.selectedIndex;
    // alert(`you chose ${month}`);
    buildCalendar(month, year)
}

function yearc(){
    let choices = document.getElementById("months");
    let choices1 = document.getElementById("years");
    year = years[choices1.selectedIndex];
    console.log("hi")

    console.log(choices1.selectedIndex);
    console.log("hi")
    month = choices.selectedIndex;
    console.log(month);
    buildCalendar(month, year)
}