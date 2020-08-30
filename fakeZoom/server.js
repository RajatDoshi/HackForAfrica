const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const { v4: uuidV4 } = require('uuid')
const path = require('path');
const ss = require('socket.io-stream')
const fs = require('fs')
const recorder = require('node-record-lpcm16');
const speech = require('@google-cloud/speech');
const {Translate} = require('@google-cloud/translate').v2;
const translate = new Translate();
// const text = 'Hello, world!';
// const target = 'ru';




const client = new speech.SpeechClient();
const encoding = 'LINEAR16';
const sampleRateHertz = 16000;
const languageCode = 'en-US';

const request = {
  config: {
    encoding: encoding,
    sampleRateHertz: sampleRateHertz,
    languageCode: languageCode,
  },
  interimResults: false, // If you want interim results, set this to true
};




app.set('view engine', 'ejs')
app.use(express.static('public'))

app.get('/', (req, res) => {
  res.render('room', { roomId: req.params.room })
  // res.redirect(`/${uuidV4()}`)

})

app.get('/:room', (req, res) => {
  res.render('room', { roomId: req.params.room })
})

io.on('connection', socket => {
  
  socket.on('join-room', (roomId, userId) => {
    
    socket.join(roomId)
    socket.to(roomId).broadcast.emit('user-connected', userId)

    socket.on('message-transcribe', async function(data) {
      console.log("reached here I thnk");
      const dataURL = data.audio.dataURL.split(',').pop();
      console.log(dataURL)
      let fileBuffer = Buffer.from(dataURL, 'base64');
      const results = await transcribeAudio(fileBuffer);
      client.emit('results', results);
    });

    socket.on('languageButton', async function(message, lang){
      console.log("reaching here at least");
      const results = await translateText(message, lang);
      socket.emit('langData', results);
    })



    socket.on('readFile', () =>{
      var dat;
      fs.readFile('/Users/roshanwarman/Downloads/practiceGoogleAPI/output.txt', function (err, data) {
        if (err) {
           return console.error(err);
        }
        socket.emit('fileData', data.toString())

     });

    })
    socket.on('disconnect', () => {
      socket.to(roomId).broadcast.emit('user-disconnected', userId)
    })

    
  })

})

async function transcribeAudio(audio){
  request.audio = {
    content: audio
  };
  console.log(audio)
  const responses = await client.recognize(request);
  console.log(responses.results)
  const transcription = response.results.map(result => result.alternatives[0].transcript).join('\n');
  console.log(`Transcription: ${transcription}`);
  return transcription;
}

async function translateText(text, target) {
  let final;
  let [translations] = await translate.translate(text, target);
  translations = Array.isArray(translations) ? translations : [translations];
  console.log('Translations:');
  translations.forEach((translation, i) => {
    console.log(`${translation}`);
    final = translation;
  });
  return final;
  
}

server.listen(3000)