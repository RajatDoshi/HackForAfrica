let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
let years = [2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031];

// for(let i = 0; i < 2100; i++){
//     years.push(i);
//     document.createElement("")
// }



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


// class dateAndTime{

// }

let day = new Date()
let month;
let year;
let doctorDays = [];
let ghettoTarget;
let SelectedDates = new Map();
let timesSelected = [];
// let tbl = document.querySelector(".Calendar")

// console.log(months[day.getMonth()])
// console.log(daysInMonth[months[day.getMonth()]])

// document.addEventListener("click", function(element){
//     doctorDays = [];
//     let selected = document.getElementsByClassName("circle")
//     let len = selected.length;
//     for(var i = 0; i < len;i++ ){
//         doctorDays.push(selected[i].innerHTML);
//     }
//     const specific = element.target;
//     console.log(element.target)
//     let cardDate = `${month}. ${specific.innerHTML}, ${year}`;
//     console.log(cardDate);

//     let date = document.querySelector("span.carDDate");
//     date.innerHTML = cardDate;
//     let actualCard = document.querySelector(".decideHere");
//     actualCard.style.visibility = "visible";

    
// })

document.addEventListener("CalendarDateClicked", function(e){
    doctorDays = [];
    let selected = document.getElementsByClassName("circle")
    let len = selected.length;
    for(var i = 0; i < len;i++ ){
        doctorDays.push(selected[i].innerHTML);
    }
    const specific = ghettoTarget;
    console.log(ghettoTarget)
    let cardDate = `${month}. ${specific.innerHTML}, ${year}`;
    console.log(cardDate);

    let date = document.getElementsByClassName("carDDate");
    let dlen = date.length;
    for(let i = 0; i < dlen; i++){
        date[i].innerHTML = cardDate;
    }
    let actualCard = document.querySelector(".decideHere");
    if(ghettoTarget.getAttribute("data-cardClicked") == 1){
        actualCard.style.display = "none";
        ghettoTarget.setAttribute("data-cardClicked", 0);
    }else{
        let event = new Event("timeStampsForCard");
        document.dispatchEvent(event);
        actualCard.style.display = "block";
        ghettoTarget.setAttribute("data-cardClicked", 1);
    }


    
});

document.addEventListener("w", function(){
    ghettoTarget.setAttribute("data-clicked", 0);
    ghettoTarget.classList.remove("circle");

})

document.addEventListener("newTimeSelected", function(){
    console.log("newTime")
    let last = document.querySelector(".lastTime");
    let newT = document.createElement("select");
    let defaul = document.createElement("option");
    defaul.innerHTML = "--Choose Time--"
    defaul.selected = true;
    newT.appendChild(defaul);
    hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    minutes = ["00",30]
    let hlen = hours.length;
    let mlen = minutes.length;
    for(let i = 0; i < hlen; i++){
        for(let j = 0; j < mlen; j++){
            let opt = document.createElement("option");

            if(j < mlen -1){
                opt.innerHTML = `${hours[i]}:${minutes[j]} — ${hours[i]}:${minutes[(j+1)%mlen]}`;
            }else if(j == mlen - 1 && i < hlen -1){
                opt.innerHTML = `${hours[i]}:${minutes[j]} — ${hours[i+1]}:${minutes[(j+1)%mlen]}`;
            }else{
                opt.innerHTML = "23:30 —— 0:00";
            }
            newT.appendChild(opt);
        }
    }

    last.classList.remove("lastTime");
    newT.classList.add("lastTime");
    newT.classList.add("oneTimeStamp");
    last.parentNode.insertBefore(newT, last.nextSibling);

});

document.addEventListener("TimeSaved", function(){

})


document.addEventListener("DOMContentLoaded", function(){
    year = day.getFullYear(); 
    month = months[day.getMonth()];
    document.getElementById("months").selectedIndex = day.getMonth();
    document.getElementById("years")
    let f = new Date();
   buildCalendar(f.getMonth(), f.getFullYear());
})

// alert(`${year} and ${month}`)
// document.getElementById("MyElement").classList.add('MyClass');



let tbl = document.querySelector(".Calendar");

function buildCalendar(month, year){
    tbl.innerHTML = " <tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>";
    let f= new Date();
    let todayDay = f.getDate();
    let todayMonth = f.getMonth();
    let todayYear = f.getFullYear();
    // let m = document.createElement("h1");
    // m.innerHTML = months[month];
    // document.body.append(m);
    // let y = document.createElement("h1");
    // y.innerHTML = year;
    // document.body.append(y);
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

            let dat = document.createElement("td");
            let sp = document.createElement("span");
            sp.setAttribute("data-day", dates);
            sp.setAttribute("data-clicked", 0);
            sp.setAttribute("data-cardClicked", 0)
            sp.style.lineHeight = 2;
            if(index < dayNum){
                sp.innerHTML = "";
                rw.appendChild(dat);
                continue;
            }
            if(index < dayR+dayNum){
                sp.innerHTML =  dates;
                if(dates == todayDay && todayMonth == month && todayYear == year){
                    sp.classList.add("today");
                }
                dates++;
                sp.classList.add("fal");
                sp.classList.add("hvr-sweep-to-right");
                sp.onclick = function(){  
                    cValue = sp.getAttribute("data-clicked")
                    if( cValue == 0){
                        sp.setAttribute("data-clicked", 1);
                        sp.classList.add("circle");
                    }
                    // else{
                    //     sp.setAttribute("data-clicked", 0);
                    //     sp.classList.remove("circle");
                    // }

                    const event = new Event("CalendarDateClicked");
                    ghettoTarget = sp;
                    document.dispatchEvent(event);
                }
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


function monthc(){
    let choices = document.getElementById("months");
    let choices1 = document.getElementById("years");
    year = years[choices1.selectedIndex];
    monthE = choices.selectedIndex;
    // alert(`you chose ${month}`);
    buildCalendar(monthE, year)
    month = months[monthE];
}

function yearc(){
    let choices = document.getElementById("months");
    let choices1 = document.getElementById("years");
    year = years[choices1.selectedIndex];
    
    monthE = choices.selectedIndex;
    buildCalendar(monthE, year)
    month = months[monthE];
}

// function updateChosenDate(element){
//     console.log("hello")
//     cValue = element.getAttribute("data-clicked")
//     if( cValue == 0){
//         element.setAttribute("data-clicked", 1);
//         element.classList.add("circle");
//     }else{
//         element.setAttribute("data-clicked", 0);
//         element.classList.remove("circle");
//     }

//     const event = new Event("CalendarDateClicked");
//     element.dispatchEvent(event);
// }

function newTimes(){
    let event = new Event("newTimeSelected");
    document.dispatchEvent(event);
}

function saveTime(){
    timesSelected = [];
    let event = new Event("TimeSaved");
    let allTimes = document.getElementsByClassName("oneTimeStamp");
    let tlen = allTimes.length;
    for(let i = 0; i < tlen; i++){
        timesSelected.push(allTimes[i].options[allTimes[i].selectedIndex].value);
    }
    const specific = ghettoTarget;
    let cardDate = `${month}. ${specific.innerHTML}, ${year}`;
  
    SelectedDates.set(cardDate, timesSelected);

}
function unClickDateSelected(){
    const specific = ghettoTarget;
    let cardDate = `${month}. ${specific.innerHTML}, ${year}`;
  
    SelectedDates.delete(cardDate);
    let event = new Event("CalendarDateClicked");
    document.dispatchEvent(event);

    let weird = new Event("w");
    document.dispatchEvent(weird);
}