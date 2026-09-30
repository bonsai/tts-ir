#!/usr/bin/env python3
"""Provider-neutral TTS IR parser/validator.

The IR is JSONL. Provider syntax (SSML, vendor JSON, etc.) is compiled later.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

TAG_RE = re.compile(r"<[^>]+>|\[[^\]]+\]|\{\{[^}]+\}\}")


def parse_line(line: str, line_no: int) -> dict[str, Any]:
    obj = json.loads(line)
    if not isinstance(obj, dict) or "op" not in obj:
        raise ValueError(f"line {line_no}: expected JSON object with 'op'")
    return obj


def validate_record(obj: dict[str, Any], line_no: int) -> None:
    op = obj.get("op")
    if op == "say":
        text = obj.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"line {line_no}: say.text must be non-empty")
        if TAG_RE.search(text):
            raise ValueError(
                f"line {line_no}: say.text contains markup; "
                "compile semantic tags into IR operations before TTS"
            )
    elif op == "pause":
        if not isinstance(obj.get("ms"), (int, float)) or obj["ms"] < 0:
            raise ValueError(f"line {line_no}: pause.ms must be >= 0")
    elif op == "speaker":
        if not isinstance(obj.get("speaker"), str) or not obj["speaker"].strip():
            raise ValueError(f"line {line_no}: speaker.speaker required")
    elif op == "style":
        if not isinstance(obj.get("style"), str) or not obj["style"].strip():
            raise ValueError(f"line {line_no}: style.style required")
    else:
        raise ValueError(f"line {line_no}: unknown op: {op!r}")


def validate(path: Path) -> int:
    errors = 0
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            validate_record(parse_line(raw, line_no), line_no)
        except (ValueError, json.JSONDecodeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            errors += 1
    if errors:
        print(f"validation failed: {errors} error(s)", file=sys.stderr)
        return 1
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "validate":
        print("usage: tts_ir.py validate FILE.jsonl", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(validate(Path(sys.argv[2])))
