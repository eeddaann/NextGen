import { convertAudioBufferToWavBlob, uploadBlob, initButtonListener } from './utils.js';


  // Initialize variables now that media devices are ready
  //const mediaRecorder = new MediaRecorder(stream);
  //let audioChunks = [];
  //initButtonListener(mediaRecorder);
  function GetPrefix() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if(urlParams.has('exp_input')){
      return urlParams.get('exp_input')
    } else {
      return 'recording'
    }
  }
  // When the recording has stopped, process and download our audio
  async function sendToServer(webaBlob) {

    // Convert the blob into binary data
    const arrayBuffer = await webaBlob.arrayBuffer();

    // Use AudioContext to decode our array buffer into an audio buffer
    const audioContext = new AudioContext();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    const wavBlob = await convertAudioBufferToWavBlob(audioBuffer);

    const parsedValue = await uploadBlob(wavBlob, GetPrefix());
    cnt+=1;
    document.getElementById("counter").innerHTML = cnt.toString() + " Files Uploaded!";
    function create_img() {
      document.body.innerHTML += '<img src="data:image/png;base64, '+parsedValue.plot+'";width="1000" height="500" alt="graph">'
    }
    create_img()
  }


  function record_and_send() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    const recorder = new MediaRecorder(stream);
    const chunks = [];
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = e => sendToServer(new Blob(chunks, { type: 'audio/webm;codecs=opus' }));
    setTimeout(()=> recorder.stop(), 5000); // we'll have a 5s media file
    recorder.start();
  });
 }
 // generate a new file every 5s
 let cnt = 0;
 setInterval(record_and_send, 5000);
  
