from pathlib import Path
from typing import Any
import shutil
import subprocess
import textwrap
import uuid

from PIL import Image, ImageDraw, ImageFont


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "backend" / "outputs"

VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280
VIDEO_FPS = 24


def generate_property_script(
    property_data: dict[str, Any],
) -> dict[str, Any]:
    """Generate a property video script using supplied facts."""

    property_name = str(
        property_data.get("property_name") or "Featured Property"
    ).strip()

    location = str(property_data.get("location") or "").strip()
    price = str(property_data.get("price") or "").strip()

    property_type = str(
        property_data.get("property_type") or ""
    ).strip()

    contact = str(property_data.get("contact") or "").strip()

    call_to_action = str(
        property_data.get("call_to_action") or "Enquire today"
    ).strip()

    features = property_data.get("features") or []

    if isinstance(features, str):
        features = [
            item.strip()
            for item in features.replace("\n", ",").split(",")
            if item.strip()
        ]

    features = [
        str(item).strip()
        for item in features
        if str(item).strip()
    ]

    scenes = [
        {
            "scene": 1,
            "purpose": "opening",
            "headline": property_name,
            "caption": f"Discover {property_name}",
            "duration": 4,
        }
    ]

    if location:
        scenes.append(
            {
                "scene": len(scenes) + 1,
                "purpose": "location",
                "headline": "A Place to Call Home",
                "caption": f"Located in {location}",
                "duration": 4,
            }
        )

    if property_type:
        scenes.append(
            {
                "scene": len(scenes) + 1,
                "purpose": "property_type",
                "headline": "Find Your Space",
                "caption": property_type,
                "duration": 4,
            }
        )

    for feature in features[:5]:
        scenes.append(
            {
                "scene": len(scenes) + 1,
                "purpose": "feature",
                "headline": feature,
                "caption": feature,
                "duration": 4,
            }
        )

    if price:
        scenes.append(
            {
                "scene": len(scenes) + 1,
                "purpose": "price",
                "headline": "Property Price",
                "caption": price,
                "duration": 4,
            }
        )

    final_caption = call_to_action

    if contact:
        final_caption = f"{call_to_action} | {contact}"

    scenes.append(
        {
            "scene": len(scenes) + 1,
            "purpose": "call_to_action",
            "headline": "Make Your Move",
            "caption": final_caption,
            "duration": 4,
        }
    )

    return {
        "property_name": property_name,
        "location": location,
        "scenes": scenes,
        "total_duration_seconds": sum(
            scene["duration"] for scene in scenes
        ),
        "generation_method": "template_based",
        "scene_count": len(scenes),
    }


def _find_font(bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Find a usable system font, with a Pillow fallback."""

    candidates = []

    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/Library/Fonts/Arial Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/Library/Fonts/Arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
        )

    for font_path in candidates:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, 42 if bold else 30)
            except OSError:
                continue

    return ImageFont.load_default()


def _wrap_text(text: str, width: int = 25) -> list[str]:
    """Wrap long captions to keep them readable on vertical video."""

    return textwrap.wrap(
        text,
        width=width,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [""]


def _create_scene_image(
    photo_path: Path,
    headline: str,
    caption: str,
    output_path: Path,
) -> None:
    """Create a vertical scene image with a readable caption overlay."""

    with Image.open(photo_path) as source:
        image = source.convert("RGB")

    # Crop the photo to fill a vertical 9:16 frame.
    target_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
    image_ratio = image.width / image.height

    if image_ratio > target_ratio:
        new_width = int(image.height * target_ratio)
        left = (image.width - new_width) // 2
        image = image.crop(
            (left, 0, left + new_width, image.height)
        )
    else:
        new_height = int(image.width / target_ratio)
        top = max(0, (image.height - new_height) // 2)
        image = image.crop(
            (0, top, image.width, top + new_height)
        )

    image = image.resize(
        (VIDEO_WIDTH, VIDEO_HEIGHT),
        Image.Resampling.LANCZOS,
    )

    draw = ImageDraw.Draw(image, "RGBA")

    # Add a dark translucent panel near the bottom.
    panel_top = 850

    draw.rounded_rectangle(
        (32, panel_top, VIDEO_WIDTH - 32, 1200),
        radius=24,
        fill=(16, 20, 24, 205),
    )

    headline_font = _find_font(bold=True)
    caption_font = _find_font(bold=False)

    draw.text(
        (58, panel_top + 35),
        "DWELLREEL AI  /  PROPERTY FILM",
        font=caption_font,
        fill=(239, 195, 165, 255),
    )

    y = panel_top + 105

    for line in _wrap_text(headline, width=23)[:3]:
        draw.text(
            (58, y),
            line,
            font=headline_font,
            fill=(255, 255, 255, 255),
        )
        y += 53

    y += 12

    for line in _wrap_text(caption, width=31)[:3]:
        draw.text(
            (58, y),
            line,
            font=caption_font,
            fill=(235, 237, 239, 255),
        )
        y += 39

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="JPEG", quality=92)


def render_property_video(
    storyboard: dict[str, Any],
    image_paths: list[str | Path],
) -> dict[str, Any]:
    """Render storyboard scenes and combine them into an MP4."""

    ffmpeg = shutil.which("ffmpeg")

    if not ffmpeg:
        raise RuntimeError(
            "FFmpeg was not found. Install FFmpeg and try again."
        )

    if not image_paths:
        raise ValueError("At least one property photo is required.")

    valid_images = []

    for image_path in image_paths:
        path = Path(image_path)

        if not path.is_file():
            raise ValueError(f"Property image not found: {path.name}")

        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            raise ValueError(
                f"Invalid image file: {path.name}"
            ) from exc

        valid_images.append(path)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    job_id = uuid.uuid4().hex[:12]
    job_dir = OUTPUT_DIR / f"job_{job_id}"
    scene_dir = job_dir / "scenes"
    scene_dir.mkdir(parents=True, exist_ok=True)

    scenes = storyboard["scenes"]
    concat_file = job_dir / "concat.txt"
    output_video = OUTPUT_DIR / f"property_reel_{job_id}.mp4"

    try:
        concat_entries = []

        for index, scene in enumerate(scenes):
            photo = valid_images[index % len(valid_images)]

            scene_image = scene_dir / f"scene_{index + 1:03d}.jpg"

            _create_scene_image(
                photo_path=photo,
                headline=str(scene["headline"]),
                caption=str(scene["caption"]),
                output_path=scene_image,
            )

            duration = max(1, int(scene.get("duration", 4)))

            concat_entries.append(
                f"file '{scene_image.resolve().as_posix()}'"
            )
            concat_entries.append(f"duration {duration}")

        # Repeat the last frame so FFmpeg preserves its duration.
        last_scene = scene_dir / f"scene_{len(scenes):03d}.jpg"
        concat_entries.append(
            f"file '{last_scene.resolve().as_posix()}'"
        )

        concat_file.write_text(
            "\n".join(concat_entries) + "\n",
            encoding="utf-8",
        )

        command = [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-an",
            "-vf",
            (
                f"fps={VIDEO_FPS},"
                f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:"
                "force_original_aspect_ratio=decrease,"
                f"pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:"
                "(ow-iw)/2:(oh-ih)/2,"
                "format=yuv420p"
            ),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-movflags",
            "+faststart",
            str(output_video),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg could not render the video. "
                f"Details: {result.stderr[-1500:]}"
            )

        if not output_video.is_file() or output_video.stat().st_size == 0:
            raise RuntimeError("FFmpeg did not produce a valid video file.")

        return {
            "video_filename": output_video.name,
            "video_path": str(output_video),
            "video_url": f"/outputs/{output_video.name}",
            "duration_seconds": storyboard["total_duration_seconds"],
            "scene_count": len(scenes),
            "resolution": f"{VIDEO_WIDTH}x{VIDEO_HEIGHT}",
            "format": "mp4",
        }

    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "Video rendering took too long. Try fewer or smaller photos."
        ) from exc

    finally:
        # The MP4 is saved separately; temporary scene images can be removed.
        shutil.rmtree(job_dir, ignore_errors=True)