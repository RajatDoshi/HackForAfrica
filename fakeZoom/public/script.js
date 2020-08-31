{/* <script src="https://www.WebRTC-Experiment.com/RecordRTC.js"></script> */}
const socket = io('/')

const videoGrid = document.getElementById('video-grid')
const myPeer = new Peer(undefined, {
  host: '/',
  port: '3001'
})
const myVideo = document.createElement('video')
// myVideo.muted = true
const peers = {}

navigator.mediaDevices.getUserMedia({
  audio:false,
  video: true
}).then(stream => {
  addVideoStream(myVideo, stream)

  myPeer.on('call', call => {
    call.answer(stream)
    const video = document.createElement('video')
    call.on('stream', userVideoStream => {
      addVideoStream(video, userVideoStream)
    })
  })

  socket.on('user-connected', userId => {
    connectToNewUser(userId, stream)
  })
})
let translateMessage = "default";
let translang = "sw";

//possibleLangs is the dropdown for languages to translate into
let possibleLangs = document.getElementById("patientLang");

let langEncoding = {
    "Swahili" : "sw",
    "English" : "en",
    "French" : "fr",
    "Hindi" : "hi"
}

translang = langEncoding[possibleLangs.options[possibleLangs.selectedIndex].innerHTML];
console.log(translang);
possibleLangs.onchange = function(){
  translang = langEncoding[possibleLangs.options[possibleLangs.selectedIndex].innerHTML];

}

let startb1 = document.getElementById("startbtn1")
let stopb1 = document.getElementById("stopbtn1")
let langbtn = document.getElementById("langbtn")

stopb1.onclick = function(){
  socket.emit('readFile')

}

let newEl = document.createElement("h1")
let easy = document.getElementById("easy")
socket.on('fileData', data =>{
  console.log(data)
  newEl.innerHTML = data;
  easy.appendChild(newEl);
  translateMessage = data;


})

langbtn.onclick = function(){
  socket.emit('languageButton', translateMessage, translang);
}

socket.on('langData', results =>{
  newEl.innerHTML = results;
})

let recordedAudio;
  
//   navigator.mediaDevices.getUserMedia({
//     audio:true
//   }).then(  function(stream){

//       //on broadcast this will return stream of audio
//       // socket.on('needAudio', function(){
//       //   socket.emit('googleTrasfer', stream);
//       // })
//       console.log("p");
//       recordedAudio = RecordRTC(stream, {
//         sampleRate: 44100,
//         desiredSampRate: 16000,
//         // recorderType: StereoAudioRecorder,
//         numberOfAudioChannels: 1,
//         ondataavailable : function(blob) {
//           // making use of socket.io-stream for bi-directional
//           // streaming, create a stream
//           console.log("here?")
//           var stream = ss.createStream();
//           // stream directly to server
//           // it will be temp. stored locally
//           ss(socket).emit('stream-transcribe', stream, {
//               name: 'stream.wav', 
//               size: blob.size
//           });
//           // pipe the audio blob to the read stream
//           ss.createBlobReadStream(blob).pipe(stream);
//       }
//       });

//       recordedAudio.startRecording();
//       // socket.emit('googleTransfer', stream);


//   })
// }


// startButton.onclick = function(){

//   navigator.getUserMedia({
//     audio: true
//   }).then(function(stream) {

//       console.log("BEING STREAM here")
//       //5)
//         recordAudio = RecordRTC(stream, {
//             type: 'audio',

//         //6)
//             mimeType: 'audio/webm',
//             sampleRate: 44100,
//             // used by StereoAudioRecorder
//             // the range 22050 to 96000.
//             // let us force 16khz recording:
//             desiredSampRate: 16000,
        
//             // MediaStreamRecorder, StereoAudioRecorder, WebAssemblyRecorder
//             // CanvasRecorder, GifRecorder, WhammyRecorder
//             recorderType: StereoAudioRecorder,
//             // Dialogflow / STT requires mono audio
//             numberOfAudioChannels: 1,
//             timeSlice: 4000
//     });

//     recordAudio.startRecording();
//   })
// // }

// startButton.onclick = function() {
//   // recording started

//   // make use of HTML 5/WebRTC, JavaScript getUserMedia()
//   // to capture the browser microphone stream
//   navigator.getUserMedia({
//       audio: true
//   }, function(stream) {
//           recordAudio = RecordRTC(stream, {
//           // type: 'audio',
//           // mimeType: 'audio/webm',
//           sampleRate: 16000, // this sampleRate should be the same in your server code

//           // MediaStreamRecorder, StereoAudioRecorder, WebAssemblyRecorder
//           // CanvasRecorder, GifRecorder, WhammyRecorder
//           // recorderType: StereoAudioRecorder,

//           // Dialogflow / STT requires mono audio
//           numberOfAudioChannels: 1,

//           // get intervals based blobs
//           // value in milliseconds
//           // as you might not want to make detect calls every seconds
//           // timeSlice: 4000,

//           // only for audio track
//           // audioBitsPerSecond: 128000,

//           // used by StereoAudioRecorder
//           // the range 22050 to 96000.
//           // let us force 16khz recording:
//           desiredSampRate: 16000
//       });

//       recordAudio.startRecording();
//   }, function(error) {
//       console.error(JSON.stringify(error));
//   });
// };

// stopButton.onclick = function() {
//   // stop audio recorder
//   recordAudio.stopRecording(function() {
//       // after stopping the audio, get the audio datans
//       console.log("stopped roshan is here")
//       recordAudio.getDataURL(function(audioDataURL) {

//           //2)
//           var files = {
//               audio: {
//                   type: recordAudio.getBlob().type || 'audio/wav',
//                   dataURL: audioDataURL
//               }
//           };
         
//           // submit the audio file to the server
//           socket.emit('message-transcribe', files);
//       });
//   });
// };



socket.on('results', results => {
  console.log(results);
})




socket.on('user-disconnected', userId => {
  if (peers[userId]) peers[userId].close()
})

myPeer.on('open', id => {
  socket.emit('join-room', ROOM_ID, id)
})

function connectToNewUser(userId, stream) {
  const call = myPeer.call(userId, stream);

  const video = document.createElement('video')
  call.on('stream', userVideoStream => {
    addVideoStream(video, userVideoStream)
  })
  call.on('close', () => {
    video.remove()
  })

  peers[userId] = call
}

function addVideoStream(video, stream) {
  if(videoGrid.childElementCount % 2 == 1){
    let dummy = document.createElement('div');
    dummy.classList.add("hackVideo");
    videoGrid.append(dummy);
  }
  video.srcObject = stream
  video.addEventListener('loadedmetadata', () => {
    video.play()
  });

  if(videoGrid.childElementCount > 1){
    video.style.border= "solid";
  }else{
    video.style.border = "solid rgb(152, 187, 95)";
    video.style.zIndex = "10";
  }
  video.style.marginLeft = "45px";
  video.style.marginBottom = "245px"

 

  videoGrid.append(video)

 
  
  
   
}
