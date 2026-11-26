import axios from "axios";
import type { ChatResponse, VoiceResponse } from "./types";

// All API calls go through this file.
const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"}/api/v1`,
  timeout: 30_000,
});

export async function sendChat(message: string): Promise<ChatResponse> {
  const { data } = await api.post<ChatResponse>("/chat", { message });
  return data;
}

export async function sendVoice(audio: Blob): Promise<VoiceResponse> {
  const form = new FormData();
  form.append("file", audio, "request.webm");
  const { data } = await api.post<VoiceResponse>("/voice", form);
  return data;
}
