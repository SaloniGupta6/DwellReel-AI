import asyncio
from pathlib import Path

import edge_tts


# --------------------------------------------------
# Available AI voices
# --------------------------------------------------

AVAILABLE_VOICES = {
    "en-IN-NeerjaNeural": {
        "name": "Neerja",
        "language": "Indian English",
        "gender": "Female",
    },
    "en-IN-PrabhatNeural": {
        "name": "Prabhat",
        "language": "Indian English",
        "gender": "Male",
    },
    "en-US-AriaNeural": {
        "name": "Aria",
        "language": "American English",
        "gender": "Female",
    },
    "en-US-GuyNeural": {
        "name": "Guy",
        "language": "American English",
        "gender": "Male",
    },
    "hi-IN-SwaraNeural": {
        "name": "Swara",
        "language": "Hindi",
        "gender": "Female",
    },
    "hi-IN-MadhurNeural": {
        "name": "Madhur",
        "language": "Hindi",
        "gender": "Male",
    },
}


# --------------------------------------------------
# Narration validation
# --------------------------------------------------

def validate_script(text: str) -> str:
    text = " ".join(str(text or "").split())

    if not text:
        raise ValueError(
            "Narration text cannot be empty."
        )

    if len(text) > 5000:
        raise ValueError(
            "Narration cannot exceed 5000 characters."
        )

    return text


# --------------------------------------------------
# Generate AI narration
# --------------------------------------------------

async def generate_voice_async(
    text: str,
    output_path: str,
    voice: str = "en-IN-NeerjaNeural",
) -> str:

    text = validate_script(text)

    if voice not in AVAILABLE_VOICES:
        raise ValueError(
            f"Unsupported voice: {voice}"
        )

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if output_file.suffix.lower() != ".mp3":
        raise ValueError(
            "Narration output must use the MP3 format."
        )

    try:
        communicator = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate="+0%",
            volume="+0%",
            pitch="+0Hz",
        )

        await communicator.save(
            str(output_file)
        )

    except Exception as exc:
        raise RuntimeError(
            f"AI voice generation failed: {exc}"
        ) from exc

    if (
        not output_file.exists()
        or output_file.stat().st_size == 0
    ):
        raise RuntimeError(
            "AI narration file was not generated."
        )

    return str(output_file.resolve())


# --------------------------------------------------
# Synchronous helper
# --------------------------------------------------

def generate_voice(
    text: str,
    output_path: str,
    voice: str = "en-IN-NeerjaNeural",
) -> str:

    return asyncio.run(
        generate_voice_async(
            text=text,
            output_path=output_path,
            voice=voice,
        )
    )