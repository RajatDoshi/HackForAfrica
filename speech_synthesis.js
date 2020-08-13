//Variable that actually performs the text to speech
var synth = window.speechSynthesis;

//If we want a form or input of text to be converted to speech
//Used this for initial coding tests; keep for future debugging
//var inputForm = document.querySelector('form');
//var inputTxt = document.querySelector('.txt');

//var voiceSelect = document.querySelector('select');

//var pitch = document.querySelector('#pitch');
var pitchValue = 1 //Subject to change
//var rate = document.querySelector('#rate');
var rateValue = 0.8 //Subject to change

var voices = [];

function populateVoiceList()
{
  voices = synth.getVoices().sort(function (a, b)
  {
    const aname = a.name.toUpperCase(), bname = b.name.toUpperCase();
    if ( aname < bname ) return -1;
    else if ( aname == bname ) return 0;
    else return +1;
      //Was for internal purposes of alphabetizing voices
  }
  );

  //Additional functionality of having a choice of the different voices (accents) if needed

  //var selectedIndex = voiceSelect.selectedIndex < 0 ? 0 : voiceSelect.selectedIndex;
  //voiceSelect.innerHTML = '';
  // for(i = 0; i < voices.length ; i++) {
  //   var option = document.createElement('option');
  //   option.textContent = voices[i].name + ' (' + voices[i].lang + ')';
    
  //   if(voices[i].default) {
  //     option.textContent += ' -- DEFAULT';
  //   }

  //   option.setAttribute('data-lang', voices[i].lang);
  //   option.setAttribute('data-name', voices[i].name);
  //   voiceSelect.appendChild(option);
  // }
  // voiceSelect.selectedIndex = selectedIndex;
}

populateVoiceList();
if (speechSynthesis.onvoiceschanged !== undefined)
{
  speechSynthesis.onvoiceschanged = populateVoiceList;
}

function speak(elmt){
    if (synth.speaking)
    {
        console.error('speechSynthesis.speaking');
        return;
    }
    if (elmt !== '')
    {
    //Just calling this var utterance b/c of the class name lmao
    var utterance = new SpeechSynthesisUtterance(elmt);
    utterance.onend = function (event)
    {
        console.log('SpeechSynthesisUtterance.onend');
    }
    utterance.onerror = function (event)
    {
        console.error('SpeechSynthesisUtterance.onerror');
    }
    //Removed this line afterward since we are sticking with one fixed voice
    //var selectedOption = voiceSelect.selectedOptions[0].getAttribute('data-name');
    for(i = 0; i < voices.length ; i++)
    {
      if(voices[i].name === "Google US English")
      {
        utterance.voice = voices[i];
        break;
      }
    }
    utterance.pitch = pitchValue;
    //Setting the rate to fixed at 0.85 so people less comfortable with English can hear but it isn't too slow
    utterance.rate = rateValue;
    synth.speak(utterance);
    //document.write(selectedOption)
    //document.write(inputTxt.value)
  }
}

// inputForm.onsubmit = function(event) {
//   event.preventDefault();

//   speak();

//   inputTxt.blur();
// }
//For if we want to give them the option of pitch/rate
// pitch.onchange = function() {
//   pitchValue.textContent = pitch.value;
// }

// rate.onchange = function() {
//   rateValue.textContent = rate.value;
// }
//For aforementioned functionality of choosing voice/accent
// voiceSelect.onchange = function(){
//   speak();
// }