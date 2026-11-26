# Eval audio clips

Every team member records 10 to 15 clips in their own language mix. Pair 1 uses them to test speech to text; Pair 2 collects and labels them.

- Format: `.webm`, `.m4a`, `.mp3` or `.wav`, under 30 seconds
- Name: `<language>-<speaker>-<number>.<ext>`, for example `te-pavan-001.webm`
- Add one line per clip to `labels.jsonl`: `{"file": "te-pavan-001.webm", "transcript": "...", "expected": {...}}`
- Record in normal conditions (some background noise is good)
- Do not include real phone numbers or home addresses
