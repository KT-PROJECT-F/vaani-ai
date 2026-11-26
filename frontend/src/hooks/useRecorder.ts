import { useRef, useState } from "react";

// Records microphone audio with the browser MediaRecorder API (free, no library).
export function useRecorder() {
  const [recording, setRecording] = useState(false);
  const recorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);

  async function start() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream);
    chunks.current = [];
    rec.ondataavailable = (e) => chunks.current.push(e.data);
    rec.start();
    recorder.current = rec;
    setRecording(true);
  }

  function stop(): Promise<Blob> {
    return new Promise((resolve) => {
      const rec = recorder.current;
      if (!rec) return resolve(new Blob());
      rec.onstop = () => {
        rec.stream.getTracks().forEach((t) => t.stop());
        resolve(new Blob(chunks.current, { type: "audio/webm" }));
      };
      rec.stop();
      setRecording(false);
    });
  }

  return { recording, start, stop };
}
