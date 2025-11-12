let isRecording = false;
let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById('recordBtn');
const statusText = document.getElementById('status');

recordBtn.addEventListener('click', async () => {
  if (!isRecording) {
    // Start recording
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      statusText.innerText = "Analyzing emotion...";

      try {
        const response = await fetch("http://127.0.0.1:5000/detect-emotion", {
          method: "POST",
          body: formData
        });

        const data = await response.json();
        if (data.emotion) {
          statusText.innerText = `Detected Emotion: ${data.emotion}`;
        } else {
          statusText.innerText = `Error: ${data.error || "Unknown issue"}`;
        }
      } catch (error) {
        console.error("❌ Fetch error:", error);
        statusText.innerText = "Error sending audio to backend.";
      }
    };

    mediaRecorder.start();
    isRecording = true;
    recordBtn.innerText = "Stop Recording";
    statusText.innerText = "Recording...";
  } else {
    // Stop recording
    mediaRecorder.stop();
    isRecording = false;
    recordBtn.innerText = "Start Recording";
  }
});
