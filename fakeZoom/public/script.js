const recorder = require('node-record-lpcm16');

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



navigator.mediaDevices.getUserMedia({
  audio:true,
  video:false
}).then(  function(stream){

    //on broadcast this will return stream of audio
    socket.on('needAudio', function(){
      socket.emit('googleTrasfer', stream);
    })


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