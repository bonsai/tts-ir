from tts_ir import validate_record


def test_plain_say():
    validate_record({"op": "say", "text": "こんにちは。"}, 1)


def test_markup_is_rejected():
    try:
        validate_record({"op": "say", "text": "こんにちは <break time='500ms'/>"}, 1)
    except ValueError:
        return
    raise AssertionError("markup must not reach TTS")


def test_semantic_pause_is_valid():
    validate_record({"op": "pause", "ms": 500}, 1)
