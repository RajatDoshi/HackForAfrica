let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
let years = [2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031];
let optionlist = [];


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

/*
Calendar instructions: User clicks on the number of the calendar. SelectedDates is a hashtable with keys of the days 
in the form "month. day, year" and maps to an array of all the selected times. 
*/


let day = new Date()
let month;
let year;
let doctorDays = [];
let ghettoTarget;
let SelectedDates = new Map();
let timesSelected = [];




document.addEventListener("CalendarDateClicked", function(e){
    // doctorDays = [];

    // let selected = document.getElementsByClassName("circle")
    // let len = selected.length;
    // for(var i = 0; i < len;i++ ){
    //     if(selected[i] == ghettoTarget){
    //         // console.log(selected[i].innerHTML);
    //         // console.log(selected[i].getAttribute("data-clicked"))
    //     }
    //     // console.log(selected[i].getAttribute("data-clicked"))
    //     if(selected[i] != ghettoTarget && selected[i].getAttribute("data-savedTime") == 0){
    //         selected[i].setAttribute("data-clicked", 0);
    //         selected[i].setAttribute("data-cardClicked", 0);
    //         selected[i].classList.remove("circle");
    //     }
    // }
    const specific = ghettoTarget;
    // console.log(ghettoTarget)
    let cardDate = `${month}. ${specific.innerHTML}, ${year}`;
    // console.log(cardDate);

    let date = document.getElementsByClassName("carDDate");
    let dlen = date.length;
    for(let i = 0; i < dlen; i++){
        // console.log(date[i])
        date[i].innerHTML = cardDate;
    }
    let actualCard = document.querySelector(".decideHere");
    if(ghettoTarget.getAttribute("data-savedTime") == 1 && ghettoTarget.getAttribute("data-clicked") == 0){

        let event = new Event("TimeSaved");
        document.dispatchEvent(event);
        actualCard.style.display = "block";
        ghettoTarget.setAttribute("data-clicked", 1);

    }else if(ghettoTarget.getAttribute("data-savedTime") == 1 && ghettoTarget.getAttribute("data-clicked") == 1){
        let event = new Event("TimeSaved");
        document.dispatchEvent(event);
        ghettoTarget.setAttribute("data-clicked", 0);

    }else if(ghettoTarget.getAttribute("data-clicked") == 1 && ghettoTarget.getAttribute("data-savedTime") == 0){

        actualCard.style.display = "none";
        ghettoTarget.setAttribute("data-cardClicked", 0);
        ghettoTarget.setAttribute("data-clicked", 0);
        ghettoTarget.classList.remove("circle");
        SelectedDates.delete(cardDate);

    }else{
        //data-clicked = 0 and not saved-time
        actualCard.style.display = "block";
        ghettoTarget.setAttribute("data-cardClicked", 1);
        ghettoTarget.setAttribute("data-clicked", 1);
        ghettoTarget.classList.add("circle");
        let event = new Event("TimeNotSaved");
        document.dispatchEvent(event);
    }

    doctorDays = [];

    let selected = document.getElementsByClassName("circle")
    let len = selected.length;
    for(var i = 0; i < len;i++ ){
        if(selected[i] == ghettoTarget){
            // console.log(selected[i].innerHTML);
            // console.log(selected[i].getAttribute("data-clicked"))
        }
        // console.log(selected[i].getAttribute("data-clicked"))
        if(selected[i] != ghettoTarget && selected[i].getAttribute("data-savedTime") == 0){
            selected[i].setAttribute("data-clicked", 0);
            selected[i].setAttribute("data-cardClicked", 0);
            selected[i].classList.remove("circle");
        }
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
    ghettoTarget.setAttribute("data-savedTime", 1);
    let cardDate = `${month}. ${ghettoTarget.innerHTML}, ${year}`;
    let cBody = document.querySelector("div.card-body");
    cBody.innerHTML = "";
    let timesOnThisDate = SelectedDates.get(cardDate);
    let tlen = timesOnThisDate.length;
    let instruction = document.createElement("h5");
    instruction.classList.add("card-title")
    instruction.innerHTML = `Your selected times on ${cardDate}:`;
    cBody.appendChild(instruction);
    for(let i = 0; i < tlen; i++){
        let list = document.createElement("div");
        list.classList.add("card-text");
        list.innerHTML = timesOnThisDate[i];
        console.log(list.innerHTML);
        cBody.appendChild(list);
    }

    let deleteButton = document.createElement("div");
    deleteButton.classList.add("card-text");
    deleteButton.innerHTML = `Delete ${cardDate} from my schedule.`
    cBody.appendChild(deleteButton);
    deleteButton.onclick = function(){unClickDateSelected()};
})

document.addEventListener("TimeNotSaved", function(){
   
    ghettoTarget.setAttribute("data-savedTime", 0);
    let cBody = document.querySelector("div.card-body");
    let cardDate = `${month}. ${ghettoTarget.innerHTML}, ${year}`;
    // cBody.innerHTML = "";
    cBody.innerHTML= ` <h5 class="card-title">What times work well for <span style = "color:rgb(187, 8, 8)">you</span> on <span class = "carDDate">${cardDate}</span>?</h5>
    <select id = "times" class = "oneTimeStamp lastTime">
        <option selected>--Choose Time--</option>
    </select>

    <div></div>
    <div onclick = newTimes()>Add more times.</div>
    <div></div>
    <a onclick = unClickDateSelected()>Remove <span class = "carDDate">${cardDate}</span></a>
    <div></div>
    <div onclick = saveTime()>Save times.</div>`;

    let event = new Event("timeStampsForCard");
    document.dispatchEvent(event);

});


document.addEventListener("DOMContentLoaded", function(){
    year = day.getFullYear(); 
    month = months[day.getMonth()];
    document.getElementById("months").selectedIndex = day.getMonth();
    document.getElementById("years")
    let f = new Date();
    buildCalendar(f.getMonth(), f.getFullYear());
    let x = document.getElementsByClassName("fal");

    //mont. day, year : arroftimes

    //for key, vlaue in dict:
        // x[key.day - 1].click();
        // timeSelected= value;
        // saveTime2();
    x[10].click();
    
    // let time = document.getElementById("times");
    // let tlen = time.options.length;
    // for(let i = 0; i <tlen; i++){
    //     optionlist.push(time.options[i].innerHTML);
    // }
    // console.log(whichIndex(optionlist, "3:00 — 3:30"))
    timesSelected = ["1:00 — 1:30", "3:00 — 3:30"];
    saveTime2();
    x[22].click()
    timesSelected = ["3:00 — 3:30", "5:00 — 5:30"];
    saveTime2();



})



let tbl = document.querySelector(".Calendar");

function buildCalendar(month, year){
    tbl.innerHTML = " <tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>";
    let f= new Date();
    let todayDay = f.getDate();
    let todayMonth = f.getMonth();
    let todayYear = f.getFullYear();
  
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
            sp.setAttribute("data-savedTime", 0);
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
                // sp.classList.add("hvr-sweep-to-right");
                sp.classList.add("hvr-radial-out");

                sp.onclick = function(){  
                    // cValue = sp.getAttribute("data-clicked")
                    // console.log(cValue);
                    // if( cValue == 0){
                    //     console.log("read")
                    //     sp.setAttribute("data-clicked", 1);
                    //     sp.classList.add("circle");
                    // }
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
    document.dispatchEvent(event);

}

function saveTime2(){

    let event = new Event("TimeSaved");
    const specific = ghettoTarget;
    let cardDate = `${month}. ${specific.innerHTML}, ${year}`;  
    SelectedDates.set(cardDate, timesSelected);
    document.dispatchEvent(event);
}

function whichIndex(arr, value){
    let len  = arr.length;
    for(let i = 0; i < len; i++){
        if(arr[i] == value){
            return i;
        }
    }
    return -1;
}
function unClickDateSelected(){
    const specific = ghettoTarget;
    let cardDate = `${month}. ${specific.innerHTML}, ${year}`;
    console.log("gettin called")
    SelectedDates.delete(cardDate);
    ghettoTarget.setAttribute("data-savedTime", 0);
    ghettoTarget.setAttribute("data-clicked", 1);
    let event = new Event("CalendarDateClicked");
    document.dispatchEvent(event);

    let weird = new Event("w");
    document.dispatchEvent(weird);
}

