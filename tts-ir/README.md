# TTS IR

TTS Intermediate Representation for `youtube-3min`.

The IR describes **how a talk should be spoken**, independently of any TTS provider. Providers such as SSML-based engines can be compiler targets.

## Pipeline

`talk.md → TTS IR (JSONL) → provider compiler → TTS → audio`

The IR is semantic: `pause`, `emphasis`, `rate`, `speaker`, and `role` describe intent rather than provider-specific syntax.

## Minimal operations

- `say`: spoken text
- `pause`: silence in milliseconds
- `speaker`: switch speaker
- `style`: named reading style
- `emphasis`: emphasis level

Example:

```jsonl
{"op":"say","text":"今日はTTSについて話します。"}
{"op":"pause","ms":500}
{"op":"say","text":"ここがポイントです。","emphasis":"strong"}
{"op":"say","text":"少しゆっくり話します。","rate":0.85}
{"op":"say","text":"……まあ、知らんけど。","role":"aside"}
```

Keep this layer provider-neutral. Compilation to SSML or a provider API belongs downstream.
