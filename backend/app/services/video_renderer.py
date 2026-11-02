import shutil
import subprocess
import textwrap
from pathlib import Path
from typing import Any


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "backend" / "outputs"

FFMPEG_PATH = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Each property photo stays on screen for 6 seconds.
SCENE_DURATION = 6.0

# Smooth crossfade between scenes.
TRANSITION_DURATION = 0.8

# Cinematic zoom.
ZOOM_INCREMENT = 0.0005
MAX_ZOOM = 1.06

# Background music becomes softer when narration exists.
MUSIC_DUCKING_FACTOR = 0.25

# Narration volume.
NARRATION_VOLUME = 1.0

# Final property information panel duration.
CLOSING_DURATION = 4.0


# ============================================================
# FONT
# ============================================================

def _find_font() -> str:

    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]

    for candidate in candidates:

        if Path(candidate).is_file():
            return candidate

    return ""


# ============================================================
# TEXT HELPERS
# ============================================================

def _escape_filter_path(value: str) -> str:

    value = str(value)

    value = value.replace("\\", "\\\\")
    value = value.replace(":", "\\:")
    value = value.replace("'", "\\'")
    value = value.replace(",", "\\,")
    value = value.replace("[", "\\[")
    value = value.replace("]", "\\]")

    return value


def _clean_text(
    value: Any,
    fallback: str = "",
) -> str:

    result = " ".join(
        str(value or "").split()
    )

    return result if result else fallback


def _wrap_text(
    value: str,
    width: int = 30,
) -> str:

    value = _clean_text(value)

    if not value:
        return ""

    return "\n".join(
        textwrap.wrap(
            value,
            width=width,
            break_long_words=True,
            break_on_hyphens=False,
        )
    )


def _write_text_file(
    directory: Path,
    filename: str,
    content: str,
) -> Path:

    path = directory / filename

    path.write_text(
        content,
        encoding="utf-8",
    )

    return path


# ============================================================
# FFMPEG EXECUTION
# ============================================================

def _run_ffmpeg(command: list[str]) -> None:

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )

    if result.returncode != 0:

        raise RuntimeError(
            "FFmpeg failed to render the property video.\n"
            + result.stderr[-10000:]
        )


# ============================================================
# BACKGROUND MUSIC FILTER
# ============================================================

def _build_music_filter(
    input_index: int,
    duration: float,
    audio_volume: float,
    audio_start_time: float,
    fade_in: float,
    fade_out: float,
    narration_enabled: bool,
) -> str:

    effective_volume = audio_volume

    if narration_enabled:

        effective_volume *= MUSIC_DUCKING_FACTOR

    filters = [
        f"atrim=start={audio_start_time:.3f}",
        "asetpts=PTS-STARTPTS",
        f"volume={effective_volume:.3f}",
    ]

    if fade_in > 0:

        effective_fade_in = min(
            fade_in,
            duration,
        )

        filters.append(
            f"afade=t=in:st=0:d={effective_fade_in:.3f}"
        )

    if fade_out > 0:

        effective_fade_out = min(
            fade_out,
            duration,
        )

        fade_start = max(
            0.0,
            duration - effective_fade_out,
        )

        filters.append(
            f"afade=t=out:st={fade_start:.3f}:"
            f"d={effective_fade_out:.3f}"
        )

    filters.extend([
        f"apad=whole_dur={duration:.3f}",
        f"atrim=duration={duration:.3f}",
        "asetpts=PTS-STARTPTS",
    ])

    return (
        f"[{input_index}:a:0]"
        + ",".join(filters)
        + "[music]"
    )


# ============================================================
# AI NARRATION FILTER
# ============================================================

def _build_narration_filter(
    input_index: int,
    duration: float,
) -> str:

    return (
        f"[{input_index}:a:0]"
        f"atrim=duration={duration:.3f},"
        "asetpts=PTS-STARTPTS,"
        f"volume={NARRATION_VOLUME:.2f},"
        f"apad=whole_dur={duration:.3f},"
        f"atrim=duration={duration:.3f},"
        "asetpts=PTS-STARTPTS"
        "[narration]"
    )


# ============================================================
# MAIN VIDEO RENDERER
# ============================================================

def render_property_video(
    image_paths: list[str],
    storyboard: dict[str, Any],
    output_filename: str,
    audio_path: str | None = None,
    audio_volume: float = 0.7,
    audio_start_time: float = 0.0,
    fade_in: float = 1.0,
    fade_out: float = 1.5,
    loop_audio: bool = True,
    narration_path: str | None = None,
) -> str:

    """
    Render a vertical real-estate promotional video.

    Features:
    - 1080 x 1920 portrait output.
    - Six-second property scenes.
    - Blurred full-screen image backgrounds.
    - Original property photos displayed in foreground.
    - Cinematic zoom animation.
    - Smooth crossfade transitions.
    - Headlines and captions.
    - Branding.
    - Property closing information.
    - Optional background music.
    - Optional AI narration.
    - Automatic background music attenuation.
    - Music volume and fade controls.
    - H.264 video and AAC audio.

    Returns:
        Absolute path to generated MP4.
    """

    # ========================================================
    # 1. VALIDATE INPUTS
    # ========================================================

    if not 4 <= len(image_paths) <= 8:

        raise ValueError(
            "Upload between 4 and 8 property photos."
        )

    if not Path(FFMPEG_PATH).is_file():

        raise RuntimeError(
            f"FFmpeg was not found at {FFMPEG_PATH}."
        )

    for image_path in image_paths:

        if not Path(image_path).is_file():

            raise FileNotFoundError(
                f"Property image not found: {image_path}"
            )

    if audio_path is not None:

        if not Path(audio_path).is_file():

            raise FileNotFoundError(
                f"Background music not found: {audio_path}"
            )

        if not 0.0 <= audio_volume <= 1.0:

            raise ValueError(
                "Audio volume must be between 0 and 1."
            )

        if audio_start_time < 0:

            raise ValueError(
                "Audio start time cannot be negative."
            )

        if fade_in < 0 or fade_out < 0:

            raise ValueError(
                "Fade durations cannot be negative."
            )

    if narration_path is not None:

        if not Path(narration_path).is_file():

            raise FileNotFoundError(
                f"Narration file not found: {narration_path}"
            )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_filename = Path(output_filename).name

    if not output_filename.lower().endswith(".mp4"):

        output_filename += ".mp4"

    output_path = OUTPUT_DIR / output_filename

    # ========================================================
    # 2. PROPERTY INFORMATION
    # ========================================================

    property_name = _clean_text(
        storyboard.get("property_name"),
        "EXCLUSIVE PROPERTY",
    )

    location = _clean_text(
        storyboard.get("location")
    )

    price = _clean_text(
        storyboard.get("price")
    )

    property_type = _clean_text(
        storyboard.get("property_type")
    )

    contact = _clean_text(
        storyboard.get("contact")
    )

    call_to_action = _clean_text(
        storyboard.get("call_to_action"),
        "ENQUIRE TODAY",
    )

    features = storyboard.get(
        "features",
        [],
    )

    if isinstance(features, str):

        features = [
            item.strip()
            for item in features.split(",")
            if item.strip()
        ]

    if not isinstance(features, list):

        features = []

    features = [
        str(item).strip()
        for item in features
        if str(item).strip()
    ]

    # ========================================================
    # 3. SCENE CAPTIONS
    # ========================================================

    storyboard_scenes = storyboard.get(
        "scenes",
        [],
    )

    fallback_headlines = [
        "A HOME THAT INSPIRES",
        "SPACE TO LIVE BEAUTIFULLY",
        "DESIGNED FOR COMFORT",
        "DETAILS THAT MAKE A DIFFERENCE",
        "YOUR NEXT CHAPTER STARTS HERE",
        "DISCOVER SOMETHING SPECIAL",
        "MADE FOR THE WAY YOU LIVE",
        "YOUR DREAM HOME AWAITS",
    ]

    caption_data = []

    for index in range(len(image_paths)):

        scene = (
            storyboard_scenes[index]
            if (
                isinstance(storyboard_scenes, list)
                and index < len(storyboard_scenes)
                and isinstance(
                    storyboard_scenes[index],
                    dict,
                )
            )
            else {}
        )

        headline = _clean_text(
            scene.get("headline"),
            fallback_headlines[
                index % len(fallback_headlines)
            ],
        )

        caption = _clean_text(
            scene.get("caption")
        )

        caption_data.append(
            (headline, caption)
        )

    # ========================================================
    # 4. VIDEO TIMING
    # ========================================================

    scene_count = len(image_paths)

    scene_step = (
        SCENE_DURATION - TRANSITION_DURATION
    )

    total_duration = (
        scene_count * SCENE_DURATION
        - (scene_count - 1) * TRANSITION_DURATION
    )

    total_frames = round(
        total_duration * FPS
    )

    closing_start = max(
        total_duration - CLOSING_DURATION,
        0.0,
    )

    font_path = _find_font()

    work_dir = (
        OUTPUT_DIR
        / f".render_{output_path.stem}"
    )

    work_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:

        # ====================================================
        # 5. FFMPEG INPUTS
        # ====================================================

        command = [
            FFMPEG_PATH,
            "-hide_banner",
            "-y",
            "-loglevel",
            "error",
        ]

        # Property photos.
        for image_path in image_paths:

            command.extend([
                "-loop",
                "1",
                "-framerate",
                str(FPS),
                "-t",
                str(SCENE_DURATION),
                "-i",
                str(image_path),
            ])

        # Background music.
        music_exists = audio_path is not None

        if music_exists:

            if loop_audio:

                command.extend([
                    "-stream_loop",
                    "-1",
                ])

            command.extend([
                "-i",
                str(Path(audio_path)),
            ])

        # AI narration.
        narration_exists = narration_path is not None

        if narration_exists:

            command.extend([
                "-i",
                str(Path(narration_path)),
            ])

        filter_parts = []

        # ====================================================
        # 6. PREPARE PROPERTY IMAGES
        # ====================================================

        for index in range(scene_count):

            # Split the original image into two copies:
            # One for the blurred background.
            # One for the original foreground image.

            split_filter = (
                f"[{index}:v]"
                "split=2"
                f"[bgsrc{index}]"
                f"[fgsrc{index}]"
            )

            filter_parts.append(
                split_filter
            )

            # Fill the complete vertical canvas.
            # Blur the background to avoid black bars.

            background_filter = (
                f"[bgsrc{index}]"
                f"scale={WIDTH}:{HEIGHT}:"
                "force_original_aspect_ratio=increase,"
                f"crop={WIDTH}:{HEIGHT},"
                "gblur=sigma=35,"
                "setsar=1,"
                "format=yuv420p"
                f"[bg{index}]"
            )

            filter_parts.append(
                background_filter
            )

            # Preserve the complete original property photo.

            foreground_filter = (
                f"[fgsrc{index}]"
                f"scale={WIDTH}:{HEIGHT}:"
                "force_original_aspect_ratio=decrease:"
                "force_divisible_by=2,"
                "setsar=1,"
                "format=rgba"
                f"[fg{index}]"
            )

            filter_parts.append(
                foreground_filter
            )

            # Combine blurred background and original image.

            overlay_filter = (
                f"[bg{index}][fg{index}]"
                "overlay="
                "(W-w)/2:(H-h)/2:"
                "shortest=1,"
                f"fps={FPS},"
                "setsar=1,"
                "format=yuv420p,"
                "zoompan="
                f"z='min(zoom+{ZOOM_INCREMENT},{MAX_ZOOM})':"
                "x='iw/2-(iw/zoom/2)':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS},"
                f"trim=duration={SCENE_DURATION},"
                "setpts=PTS-STARTPTS,"
                "format=yuv420p"
                f"[scene{index}]"
            )

            filter_parts.append(
                overlay_filter
            )

        # ====================================================
        # 7. CINEMATIC CROSSFADE TRANSITIONS
        # ====================================================

        current_label = "scene0"

        elapsed_duration = SCENE_DURATION

        for index in range(1, scene_count):

            output_label = f"transition{index}"

            offset = (
                elapsed_duration
                - TRANSITION_DURATION
            )

            transition_filter = (
                f"[{current_label}][scene{index}]"
                "xfade="
                "transition=fade:"
                f"duration={TRANSITION_DURATION}:"
                f"offset={offset:.3f}"
                f"[{output_label}]"
            )

            filter_parts.append(
                transition_filter
            )

            current_label = output_label

            elapsed_duration += (
                SCENE_DURATION
                - TRANSITION_DURATION
            )

        # ====================================================
        # 8. FONT CONFIGURATION
        # ====================================================

        font_option = ""

        if font_path:

            escaped_font = _escape_filter_path(
                font_path
            )

            font_option = (
                f":fontfile='{escaped_font}'"
            )

        # ====================================================
        # 9. BRANDING
        # ====================================================

        brand_path = _write_text_file(
            work_dir,
            "brand.txt",
            "DWELLREEL  /  PROPERTY FILM",
        )

        escaped_brand_path = _escape_filter_path(
            str(brand_path)
        )

        filter_parts.append(
            f"[{current_label}]"
            "drawtext="
            f"textfile='{escaped_brand_path}'"
            f"{font_option}:"
            "fontcolor=white@0.95:"
            "fontsize=24:"
            "x=72:"
            "y=100:"
            "shadowcolor=black@0.55:"
            "shadowx=1:"
            "shadowy=2"
            "[brand]"
        )

        current_label = "brand"

        # ====================================================
        # 10. HEADLINES AND CAPTIONS
        # ====================================================

        for index, (headline, caption) in enumerate(
            caption_data
        ):

            # Each scene gets its own caption interval.
            # Half the transition duration is excluded
            # at each end to prevent caption overlap.

            start_time = (
                index * scene_step
                + (
                    TRANSITION_DURATION / 2
                    if index > 0
                    else 0
                )
            )

            if index < scene_count - 1:

                end_time = (
                    (index + 1) * scene_step
                    + TRANSITION_DURATION / 2
                )

            else:

                end_time = total_duration

            # Reserve the ending for property information.

            end_time = min(
                end_time,
                closing_start,
                total_duration,
            )

            if end_time <= start_time:

                continue

            fade_duration = min(
                0.35,
                (end_time - start_time) / 2,
            )

            fade_out_start = max(
                start_time,
                end_time - fade_duration,
            )

            # Headline file.

            headline_path = _write_text_file(
                work_dir,
                f"headline_{index}.txt",
                _wrap_text(
                    headline.upper(),
                    width=27,
                ),
            )

            escaped_headline_path = _escape_filter_path(
                str(headline_path)
            )

            # Caption background panel.

            panel_label = f"panel{index}"

            filter_parts.append(
                f"[{current_label}]"
                "drawbox="
                "x=48:"
                "y=1280:"
                "w=984:"
                "h=420:"
                "color=black@0.45:"
                "t=fill:"
                f"enable='between(t,{start_time:.3f},{end_time:.3f})'"
                f"[{panel_label}]"
            )

            current_label = panel_label

            # Headline.

            headline_label = f"headline{index}"

            headline_alpha = (
                f"if(lt(t,{start_time + fade_duration:.3f}),"
                f"(t-{start_time:.3f})/{fade_duration:.3f},"
                f"if(gt(t,{fade_out_start:.3f}),"
                f"({end_time:.3f}-t)/{fade_duration:.3f},1))"
            )

            filter_parts.append(
                f"[{current_label}]"
                "drawtext="
                f"textfile='{escaped_headline_path}'"
                f"{font_option}:"
                "fontcolor=white:"
                "fontsize=60:"
                "line_spacing=15:"
                "x=80:"
                "y=1360:"
                "shadowcolor=black@0.65:"
                "shadowx=1:"
                "shadowy=3:"
                f"alpha='{headline_alpha}':"
                f"enable='between(t,{start_time:.3f},{end_time:.3f})'"
                f"[{headline_label}]"
            )

            current_label = headline_label

            # Supporting caption.

            if caption:

                caption_path = _write_text_file(
                    work_dir,
                    f"caption_{index}.txt",
                    _wrap_text(
                        caption,
                        width=43,
                    ),
                )

                escaped_caption_path = _escape_filter_path(
                    str(caption_path)
                )

                caption_label = f"caption{index}"

                filter_parts.append(
                    f"[{current_label}]"
                    "drawtext="
                    f"textfile='{escaped_caption_path}'"
                    f"{font_option}:"
                    "fontcolor=white@0.92:"
                    "fontsize=29:"
                    "line_spacing=12:"
                    "x=80:"
                    "y=1515:"
                    "shadowcolor=black@0.55:"
                    "shadowx=1:"
                    "shadowy=2:"
                    f"enable='between(t,{start_time:.3f},{end_time:.3f})'"
                    f"[{caption_label}]"
                )

                current_label = caption_label

        # ====================================================
        # 11. CLOSING INFORMATION PANEL
        # ====================================================

        closing_lines = [
            property_name.upper()
        ]

        if property_type:

            closing_lines.append(
                property_type.upper()
            )

        if location:

            closing_lines.append(
                location
            )

        if price:

            closing_lines.append(
                price
            )

        if features:

            closing_lines.append(
                "  |  ".join(features[:3])
            )

        closing_lines.append(
            call_to_action.upper()
        )

        if contact:

            closing_lines.append(
                f"CONTACT: {contact}"
            )

        closing_text = "\n\n".join(
            closing_lines
        )

        closing_path = _write_text_file(
            work_dir,
            "closing.txt",
            _wrap_text(
                closing_text,
                width=34,
            ),
        )

        escaped_closing_path = _escape_filter_path(
            str(closing_path)
        )

        # Closing background panel.

        filter_parts.append(
            f"[{current_label}]"
            "drawbox="
            "x=48:"
            "y=1390:"
            "w=984:"
            "h=470:"
            "color=black@0.78:"
            "t=fill:"
            f"enable='between(t,{closing_start:.3f},{total_duration:.3f})'"
            "[closingpanel]"
        )

        # Closing text.

        filter_parts.append(
            "[closingpanel]"
            "drawtext="
            f"textfile='{escaped_closing_path}'"
            f"{font_option}:"
            "fontcolor=white:"
            "fontsize=27:"
            "line_spacing=14:"
            "x=80:"
            "y=1430:"
            "shadowcolor=black@0.65:"
            "shadowx=2:"
            "shadowy=2:"
            f"enable='between(t,{closing_start:.3f},{total_duration:.3f})'"
            "[outv]"
        )

        # ====================================================
        # 12. AUDIO PROCESSING
        # ====================================================

        audio_labels = []

        # Background music.

        if music_exists:

            music_input_index = scene_count

            filter_parts.append(
                _build_music_filter(
                    input_index=music_input_index,
                    duration=total_duration,
                    audio_volume=audio_volume,
                    audio_start_time=audio_start_time,
                    fade_in=fade_in,
                    fade_out=fade_out,
                    narration_enabled=narration_exists,
                )
            )

            audio_labels.append(
                "music"
            )

        # AI narration.

        if narration_exists:

            narration_input_index = (
                scene_count
                + (1 if music_exists else 0)
            )

            filter_parts.append(
                _build_narration_filter(
                    input_index=narration_input_index,
                    duration=total_duration,
                )
            )

            audio_labels.append(
                "narration"
            )

        # Mix narration and background music.

        if len(audio_labels) == 2:

            filter_parts.append(
                "[narration][music]"
                "amix="
                "inputs=2:"
                "duration=longest:"
                "dropout_transition=2,"
                "alimiter=limit=0.95:"
                "level=false,"
                f"atrim=duration={total_duration:.3f},"
                "asetpts=PTS-STARTPTS"
                "[outa]"
            )

        elif len(audio_labels) == 1:

            filter_parts.append(
                f"[{audio_labels[0]}]"
                "anull[outa]"
            )

        # ====================================================
        # 13. ASSEMBLE FILTER GRAPH
        # ====================================================

        filter_complex = ";".join(
            part
            for part in filter_parts
            if part.strip()
        )

        command.extend([
            "-filter_complex",
            filter_complex,
            "-map",
            "[outv]",
        ])

        # ====================================================
        # 14. AUDIO OUTPUT
        # ====================================================

        if music_exists or narration_exists:

            command.extend([
                "-map",
                "[outa]",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                "48000",
            ])

        else:

            command.append("-an")

        # ====================================================
        # 15. VIDEO OUTPUT
        # ====================================================

        command.extend([
            "-frames:v",
            str(total_frames),
            "-r",
            str(FPS),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "19",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-metadata",
            f"title={property_name}",
            "-metadata",
            "comment=Created with DwellReel AI",
            str(output_path),
        ])

        # ====================================================
        # 16. RENDER VIDEO
        # ====================================================

        _run_ffmpeg(command)

        if (
            not output_path.is_file()
            or output_path.stat().st_size == 0
        ):

            raise RuntimeError(
                "The video renderer did not produce a valid MP4."
            )

        return str(
            output_path.resolve()
        )

    finally:

        shutil.rmtree(
            work_dir,
            ignore_errors=True,
        )