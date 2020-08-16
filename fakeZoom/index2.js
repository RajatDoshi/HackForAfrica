const recorder = require('node-record-lpcm16');
var fs = require("fs");

// Imports the Google Cloud client library
const speech = require('@google-cloud/speech');

// Creates a client
const client = new speech.SpeechClient();

/**
 * TODO(developer): Uncomment the following lines before running the sample.
 */
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

// Create a recognize stream



  const recognizeStream = client
  .streamingRecognize(request)
  .on('error', console.error)
  .on('data', data =>
      fs.writeFile("output.txt",`Transcription: ${data.results[0].alternatives[0].transcript}\n`,function (err) {
        if (err) return console.log(err);
        console.log('Hello World > helloworld.txt');
      }));
  

// Start recording and send the microphone input to the Speech API.
// Ensure SoX is installed, see https://www.npmjs.com/package/node-record-lpcm16#dependencies
recorder
  .record({
    sampleRateHertz: sampleRateHertz,
    threshold: 0,
    // Other options, see https://www.npmjs.com/package/node-record-lpcm16#options
    verbose: false,
    recordProgram: 'rec', // Try also "arecord" or "sox"
    silence: '10.0',
  }).stream()
  .pipe(recognizeStream);

console.log('Listening, press Ctrl+C to stop.');