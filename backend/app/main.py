import os
import shutil
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.app.services.video_generator import (
    generate_property_script,
)
from backend.app.services.video_renderer import (
    render_property_video,
)
from backend.app.services.voice_generator import (
    generate_voice_async,
)


# --------------------------------------------------
# Paths and directories
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

UPLOAD_DIR = PROJECT_ROOT / "backend" / "uploads"
OUTPUT_DIR = PROJECT_ROOT / "backend" / "outputs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = os.getenv(
    "DWELLREEL_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="DwellReel AI",
    description=(
        "Create real-estate videos with AI narration "
        "and background music."
    ),
    version="1.3.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Static output serving
# --------------------------------------------------

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="outputs",
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class PropertyRequest(BaseModel):
    property_name: str = Field(
        min_length=1,
        max_length=150,
    )
    location: str = ""
    price: str = ""
    property_type: str = ""
    features: list[str] = Field(default_factory=list)
    contact: str = ""
    call_to_action: str = "Enquire today"


# --------------------------------------------------
# Supported upload formats
# --------------------------------------------------

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/wave": ".wav",
    "audio/ogg": ".ogg",
    "application/ogg": ".ogg",
    "audio/aac": ".aac",
    "audio/mp4": ".m4a",
    "audio/x-m4a": ".m4a",
    "audio/m4a": ".m4a",
    "audio/webm": ".webm",
    "video/webm": ".webm",
    "audio/3gpp": ".3gp",
    "audio/3gpp2": ".3g2",
}

MAX_PHOTO_BYTES = 12 * 1024 * 1024
MAX_AUDIO_BYTES = 30 * 1024 * 1024

SUPPORTED_VOICES = {
    "en-IN-NeerjaNeural",
    "en-IN-PrabhatNeural",
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "hi-IN-SwaraNeural",
    "hi-IN-MadhurNeural",
}


# --------------------------------------------------
# Narration script generation
# --------------------------------------------------

def create_narration_script(
    property_data: dict[str, Any],
) -> str:
    """
    Create a natural narration using only the
    information supplied by the user.
    """

    parts = []

    name = property_data.get("property_name", "").strip()
    location = property_data.get("location", "").strip()
    price = property_data.get("price", "").strip()
    property_type = property_data.get(
        "property_type", ""
    ).strip()

    features = property_data.get("features", [])
    contact = property_data.get("contact", "").strip()
    cta = property_data.get(
        "call_to_action",
        "Enquire today",
    ).strip()

    if name:
        parts.append(
            f"Welcome to {name}."
        )

    if property_type:
        parts.append(
            f"Explore this {property_type}."
        )

    if location:
        parts.append(
            f"Located in {location}."
        )

    if features:
        feature_text = ", ".join(features[:6])
        parts.append(
            f"Some of its highlighted features include "
            f"{feature_text}."
        )

    if price:
        parts.append(
            f"The listed price is {price}."
        )

    if contact:
        parts.append(
            f"For more information, contact {contact}."
        )

    if cta:
        parts.append(cta + ".")

    return " ".join(parts)


# --------------------------------------------------
# Health endpoints
# --------------------------------------------------

@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to DwellReel AI",
        "status": "running",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "DwellReel AI Backend",
    }


# --------------------------------------------------
# Generate storyboard only
# --------------------------------------------------

@app.post("/api/generate-script")
def create_property_script(
    property_data: PropertyRequest,
) -> dict[str, Any]:

    try:
        return generate_property_script(
            property_data.model_dump()
        )

    except Exception as exc:
        print(f"Storyboard generation error: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate the property script.",
        ) from exc


# --------------------------------------------------
# Download generated MP4
# --------------------------------------------------

@app.get("/api/download/{filename}")
def download_property_video(
    filename: str,
) -> FileResponse:

    safe_filename = Path(filename).name

    if safe_filename != filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid video filename.",
        )

    if not safe_filename.lower().endswith(".mp4"):
        raise HTTPException(
            status_code=400,
            detail="Only MP4 downloads are supported.",
        )

    video_path = OUTPUT_DIR / safe_filename

    if not video_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Generated video not found.",
        )

    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=safe_filename,
        headers={"Cache-Control": "no-store"},
    )


# --------------------------------------------------
# Generate property video
# --------------------------------------------------

@app.post("/api/generate-video")
async def create_property_video(
    property_name: str = Form(...),
    location: str = Form(...),
    price: str = Form(...),
    property_type: str = Form(""),
    features: str = Form(""),
    contact: str = Form(""),
    call_to_action: str = Form("Enquire today"),

    # Existing background music upload
    audio: UploadFile | None = File(default=None),

    # Existing music settings
    audio_volume: float = Form(0.7),
    audio_start_time: float = Form(0.0),
    fade_in: float = Form(1.0),
    fade_out: float = Form(1.5),
    loop_audio: bool = Form(True),

    # New AI narration settings
    narration_enabled: bool = Form(False),
    narration_text: str = Form(""),
    narration_voice: str = Form("en-IN-NeerjaNeural"),

    # Property photos
    photos: list[UploadFile] = File(...),
) -> dict[str, Any]:

    request_dir: Path | None = None

    try:

        # --------------------------------------------------
        # Validate property details
        # --------------------------------------------------

        property_name = property_name.strip()
        location = location.strip()
        price = price.strip()

        if not property_name:
            raise HTTPException(
                status_code=422,
                detail="Property name is required.",
            )

        if len(property_name) > 150:
            raise HTTPException(
                status_code=422,
                detail="Property name cannot exceed 150 characters.",
            )

        if not location:
            raise HTTPException(
                status_code=422,
                detail="Property location is required.",
            )

        if not price:
            raise HTTPException(
                status_code=422,
                detail="Property price is required.",
            )

        # --------------------------------------------------
        # Validate music settings
        # --------------------------------------------------

        if not 0 <= audio_volume <= 1:
            raise HTTPException(
                status_code=422,
                detail="Audio volume must be between 0 and 1.",
            )

        if audio_start_time < 0:
            raise HTTPException(
                status_code=422,
                detail="Audio start time cannot be negative.",
            )

        if fade_in < 0 or fade_out < 0:
            raise HTTPException(
                status_code=422,
                detail="Fade durations cannot be negative.",
            )

        # --------------------------------------------------
        # Validate narration settings
        # --------------------------------------------------

        if narration_enabled:

            if narration_voice not in SUPPORTED_VOICES:
                raise HTTPException(
                    status_code=422,
                    detail="Unsupported narration voice.",
                )

            if len(narration_text) > 5000:
                raise HTTPException(
                    status_code=422,
                    detail="Narration text cannot exceed 5000 characters.",
                )

        # --------------------------------------------------
        # Validate photo count
        # --------------------------------------------------

        if not 4 <= len(photos) <= 8:
            raise HTTPException(
                status_code=422,
                detail="Upload between 4 and 8 property photos.",
            )

        # --------------------------------------------------
        # Create request directory
        # --------------------------------------------------

        request_id = uuid4().hex

        request_dir = UPLOAD_DIR / request_id

        request_dir.mkdir(
            parents=True,
            exist_ok=False,
        )

        saved_paths: list[str] = []
        audio_path: str | None = None
        narration_path: str | None = None

        # --------------------------------------------------
        # Save property photos
        # --------------------------------------------------

        for index, photo in enumerate(photos, start=1):

            content_type = (
                photo.content_type or ""
            ).lower().strip()

            extension = ALLOWED_IMAGE_TYPES.get(
                content_type
            )

            if extension is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Photo {index} must be JPG, PNG, or WEBP."
                    ),
                )

            file_path = (
                request_dir
                / f"photo_{index:02d}{extension}"
            )

            total_bytes = 0

            with file_path.open("wb") as destination:

                while True:

                    chunk = await photo.read(
                        1024 * 1024
                    )

                    if not chunk:
                        break

                    total_bytes += len(chunk)

                    if total_bytes > MAX_PHOTO_BYTES:
                        raise HTTPException(
                            status_code=413,
                            detail=f"Photo {index} exceeds 12 MB.",
                        )

                    destination.write(chunk)

            if total_bytes == 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Photo {index} is empty.",
                )

            saved_paths.append(
                str(file_path.resolve())
            )

        # --------------------------------------------------
        # Save optional background music
        # --------------------------------------------------

        if audio is not None:

            content_type = (
                audio.content_type or ""
            ).lower().split(";")[0].strip()

            extension = ALLOWED_AUDIO_TYPES.get(
                content_type
            )

            if extension is None:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported background audio format.",
                )

            audio_file_path = (
                request_dir
                / f"background_audio{extension}"
            )

            audio_bytes = 0

            with audio_file_path.open("wb") as destination:

                while True:

                    chunk = await audio.read(
                        1024 * 1024
                    )

                    if not chunk:
                        break

                    audio_bytes += len(chunk)

                    if audio_bytes > MAX_AUDIO_BYTES:
                        raise HTTPException(
                            status_code=413,
                            detail="Audio file exceeds 30 MB.",
                        )

                    destination.write(chunk)

            if audio_bytes == 0:
                raise HTTPException(
                    status_code=400,
                    detail="The uploaded audio file is empty.",
                )

            audio_path = str(
                audio_file_path.resolve()
            )

        # --------------------------------------------------
        # Parse property features
        # --------------------------------------------------

        feature_list = [
            item.strip()
            for item in (
                features
                .replace("\r", "\n")
                .replace("\n", ",")
                .split(",")
            )
            if item.strip()
        ]

        # --------------------------------------------------
        # Prepare property data
        # --------------------------------------------------

        property_data = {
            "property_name": property_name,
            "location": location,
            "price": price,
            "property_type": property_type.strip(),
            "features": feature_list,
            "contact": contact.strip(),
            "call_to_action": (
                call_to_action.strip() or "Enquire today"
            ),
        }

        # --------------------------------------------------
        # Generate storyboard
        # --------------------------------------------------

        storyboard = generate_property_script(
            property_data
        )

        if not isinstance(storyboard, dict):
            raise RuntimeError(
                "Storyboard generation returned an unexpected response."
            )

        storyboard.update(property_data)

        # --------------------------------------------------
        # Generate AI narration
        # --------------------------------------------------

        narration_script = None

        if narration_enabled:

            narration_script = (
                narration_text.strip()
                if narration_text.strip()
                else create_narration_script(property_data)
            )

            if not narration_script:
                raise HTTPException(
                    status_code=422,
                    detail="Unable to create narration from property details.",
                )

            narration_file = (
                OUTPUT_DIR
                / f"narration_{request_id[:12]}.mp3"
            )

            await generate_voice_async(
                text=narration_script,
                output_path=str(narration_file),
                voice=narration_voice,
            )

            if (
                not narration_file.is_file()
                or narration_file.stat().st_size == 0
            ):
                raise RuntimeError(
                    "AI narration generation failed."
                )

            narration_path = str(
                narration_file.resolve()
            )

        # --------------------------------------------------
        # Render final video
        # --------------------------------------------------

        video_filename = (
            f"dwellreel_{request_id[:12]}.mp4"
        )

        video_path = render_property_video(
            image_paths=saved_paths,
            storyboard=storyboard,
            output_filename=video_filename,

            # Background music
            audio_path=audio_path,
            audio_volume=audio_volume,
            audio_start_time=audio_start_time,
            fade_in=fade_in,
            fade_out=fade_out,
            loop_audio=loop_audio,

            # AI narration
            narration_path=narration_path,
        )

        video_path_obj = Path(video_path)

        if (
            not video_path_obj.is_file()
            or video_path_obj.stat().st_size == 0
        ):
            raise RuntimeError(
                "Generated MP4 is missing or empty."
            )

        # --------------------------------------------------
        # URLs
        # --------------------------------------------------

        video_name = video_path_obj.name

        video_url = (
            f"{BASE_URL}/outputs/{video_name}"
        )

        download_url = (
            f"{BASE_URL}/api/download/{video_name}"
        )

        scene_count = len(saved_paths)

        duration_seconds = (
            scene_count * 4
            - (scene_count - 1) * 0.8
        )

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return {
            "message": (
                "Premium property video generated successfully!"
            ),
            "property_name": property_name,
            "scene_count": scene_count,
            "duration_seconds": round(
                duration_seconds,
                2,
            ),
            "audio_included": (
                audio_path is not None
                or narration_path is not None
            ),
            "narration_included": (
                narration_path is not None
            ),
            "narration": {
                "enabled": narration_enabled,
                "voice": narration_voice,
                "text": narration_script,
            },
            "audio_settings": {
                "volume": audio_volume,
                "start_time": audio_start_time,
                "fade_in": fade_in,
                "fade_out": fade_out,
                "loop": loop_audio,
            } if audio_path is not None else None,
            "storyboard": storyboard,
            "video": {
                "filename": video_name,
                "video_url": video_url,
                "download_url": download_url,
                "size_bytes": video_path_obj.stat().st_size,
            },
        }

    except HTTPException:
        raise

    except Exception as exc:

        print(
            f"Property video generation error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Video generation failed. "
                f"Error: {exc}"
            ),
        ) from exc

    finally:

        # Close uploaded files
        for photo in photos:
            try:
                await photo.close()
            except Exception:
                pass

        if audio is not None:
            try:
                await audio.close()
            except Exception:
                pass

        # Remove temporary uploads
        if request_dir is not None:
            shutil.rmtree(
                request_dir,
                ignore_errors=True,
            )