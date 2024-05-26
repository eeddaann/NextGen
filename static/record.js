import { convertAudioBufferToWavBlob, uploadBlob, initButtonListener } from './utils.js';

navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
  // Initialize variables now that media devices are ready
  const mediaRecorder = new MediaRecorder(stream);
  let audioChunks = [];
  initButtonListener(mediaRecorder);

  // Listen for new audio data chunks and add them to our array
  mediaRecorder.addEventListener('dataavailable', (event) => {
    audioChunks.push(event.data);
  });

  // When the recording has stopped, process and download our audio
  mediaRecorder.addEventListener('stop', async () => {
    const webaBlob = new Blob(audioChunks, { type: 'audio/webm;codecs=opus' });

    // Convert the blob into binary data
    const arrayBuffer = await webaBlob.arrayBuffer();

    // Use AudioContext to decode our array buffer into an audio buffer
    const audioContext = new AudioContext();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    const wavBlob = await convertAudioBufferToWavBlob(audioBuffer);

    const parsedValue = await uploadBlob(wavBlob, 'recording');
    function create_img() {
      document.body.innerHTML += '<img src="data:image/png;base64, '+parsedValue.plot+'";width="1000" height="500" alt="graph">'
    }
    create_img()

    audioChunks = []; // Clear cached chunks
  });
});
