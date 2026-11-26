// Mirrors backend/app/schemas/api.py. Update both together.

export type Language = "en" | "te" | "hi" | "mixed";
export type Urgency = "emergency" | "today" | "flexible";

export interface ServiceRequest {
  service: string;
  problem: string;
  urgency: Urgency;
  city: string | null;
  area: string | null;
  time_window: string | null;
}

export interface ChatResponse {
  reply: string;
  language: Language;
  request: ServiceRequest;
  safety_steps: string[];
  price_range: [number, number] | null;
}

export interface VoiceResponse extends ChatResponse {
  transcript: string;
  stt_provider: string;
  reply_audio_base64: string | null;
}
