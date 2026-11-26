import { useState } from "react";
import { sendChat, sendVoice } from "./api/client";
import type { ChatResponse } from "./api/types";
import { ResultCard } from "./components/ResultCard";
import { useRecorder } from "./hooks/useRecorder";

const EXAMPLES = [
  "My kitchen sink is leaking badly and water is all over the floor. I need a plumber urgently this evening at Benz Circle, Vijayawada.",
  "మా ఇంట్లో కరెంట్ పోయింది, ఫ్యూజ్ ఎగిరిపోయింది. ఒక ఎలక్ట్రీషియన్‌ని గుంటూరుకి పంపండి, ఈరోజే కావాలి.",
  "Ghar mein paani nahi aa raha, please ek water tanker bhej do jaldi, Madhapur, Hyderabad.",
];

// Starter screen. TODO (Pair 4): chat history, booking cards, shadcn/ui, admin dashboard route.
export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<ChatResponse | null>(null);
  const [transcript, setTranscript] = useState<string>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const recorder = useRecorder();

  async function run(task: () => Promise<void>) {
    setLoading(true);
    setError(null);
    try {
      await task();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  function submitText(message: string) {
    if (!message.trim()) return;
    run(async () => {
      setTranscript(undefined);
      setResult(await sendChat(message));
    });
  }

  async function toggleMic() {
    if (!recorder.recording) {
      await recorder.start();
      return;
    }
    const audio = await recorder.stop();
    run(async () => {
      const res = await sendVoice(audio);
      setTranscript(res.transcript);
      setResult(res);
      if (res.reply_audio_base64) {
        new Audio(`data:audio/mpeg;base64,${res.reply_audio_base64}`).play();
      }
    });
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-6 px-4 py-10">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Vaani AI</h1>
        <p className="text-slate-600">Speak a service request in Telugu, English, Hindi or a mix.</p>
      </header>

      <button
        onClick={toggleMic}
        disabled={loading}
        className={`mx-auto flex h-24 w-24 items-center justify-center rounded-full text-white shadow-lg transition ${
          recorder.recording ? "animate-pulse bg-red-600" : "bg-indigo-600 hover:bg-indigo-700"
        } disabled:opacity-50`}
        aria-label={recorder.recording ? "Stop recording" : "Start recording"}
      >
        {recorder.recording ? "Stop" : "Speak"}
      </button>

      <form
        className="flex gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          submitText(text);
        }}
      >
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Or type your request"
          className="flex-1 rounded-xl border border-slate-300 px-4 py-2 focus:border-indigo-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-slate-900 px-4 py-2 text-white disabled:opacity-50"
        >
          Go
        </button>
      </form>

      <div className="flex flex-col gap-2">
        <p className="text-sm text-slate-500">Try an example</p>
        {EXAMPLES.map((ex) => (
          <button
            key={ex}
            onClick={() => {
              setText(ex);
              submitText(ex);
            }}
            className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-left text-sm hover:bg-slate-100"
          >
            {ex}
          </button>
        ))}
      </div>

      {loading && <p className="text-slate-500">Thinking...</p>}
      {error && <p className="rounded-xl bg-red-50 p-3 text-red-700">{error}</p>}
      {result && <ResultCard result={result} transcript={transcript} />}
    </main>
  );
}
