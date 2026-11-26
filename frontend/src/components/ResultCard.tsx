import type { ChatResponse } from "../api/types";

const urgencyStyle: Record<string, string> = {
  emergency: "bg-red-100 text-red-800",
  today: "bg-amber-100 text-amber-800",
  flexible: "bg-emerald-100 text-emerald-800",
};

export function ResultCard({ result, transcript }: { result: ChatResponse; transcript?: string }) {
  const r = result.request;
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      {transcript && <p className="mb-3 text-sm text-slate-500">You said: "{transcript}"</p>}
      <p className="whitespace-pre-line text-lg text-slate-900">{result.reply}</p>

      <dl className="mt-4 grid grid-cols-2 gap-3 text-sm">
        <Field label="Service" value={r.service.replace("_", " ")} />
        <Field label="City" value={r.city ?? "?"} />
        <Field label="Area" value={r.area ?? "?"} />
        <Field label="When" value={r.time_window ?? "?"} />
        <div>
          <dt className="text-slate-500">Urgency</dt>
          <dd>
            <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${urgencyStyle[r.urgency]}`}>
              {r.urgency}
            </span>
          </dd>
        </div>
        {result.price_range && (
          <Field label="Estimate" value={`Rs ${result.price_range[0]} to ${result.price_range[1]}`} />
        )}
      </dl>
      <p className="mt-3 text-xs text-slate-400">Detected language: {result.language}</p>
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-slate-500">{label}</dt>
      <dd className="font-medium capitalize text-slate-800">{value}</dd>
    </div>
  );
}
