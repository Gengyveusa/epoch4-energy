import os
from pathlib import Path
import urllib.request

import replicate

MODEL_VERSION = (
    "stability-ai/stable-video-diffusion:"
    "3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438"
)

FIGURES = [
    {
        "name": "pendulum",
        "image": "classical-energy.png",
        "prompt": "pendulum swinging back and forth smoothly",
    },
    {
        "name": "cosmic-budget",
        "image": "cosmic-budget.png",
        "prompt": "cosmic energy visualization with subtle particle movement",
    },
    {
        "name": "mitochondria",
        "image": "mitochondria.png",
        "prompt": "mitochondrial ATP synthesis with gentle motion",
    },
]

ROOT_DIR = Path(__file__).resolve().parent
ANIMATIONS_DIR = ROOT_DIR / "animations"


def _optional_int(env_name):
    value = os.getenv(env_name)
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Invalid integer for {env_name}: {value}") from exc


def _build_model_input(image_file):
    model_input = {"input_image": image_file}

    fps = _optional_int("SVD_FPS")
    if fps is not None:
        model_input["fps"] = fps

    motion_bucket_id = _optional_int("SVD_MOTION_BUCKET_ID")
    if motion_bucket_id is not None:
        model_input["motion_bucket_id"] = motion_bucket_id

    seed = _optional_int("SVD_SEED")
    if seed is not None:
        model_input["seed"] = seed

    video_length = os.getenv("SVD_VIDEO_LENGTH")
    if video_length:
        model_input["video_length"] = video_length

    return model_input


def generate_animation(image_path, prompt):
    with open(image_path, "rb") as image_file:
        model_input = _build_model_input(image_file)
        output = replicate.run(MODEL_VERSION, input=model_input)
    return output


def _resolve_output_url(output):
    if output is None:
        return None
    if isinstance(output, dict):
        for value in output.values():
            url = _resolve_output_url(value)
            if url:
                return url
        return None
    if isinstance(output, (list, tuple)):
        for item in output:
            url = _resolve_output_url(item)
            if url:
                return url
        return None
    if isinstance(output, (str, bytes)):
        return output
    url = getattr(output, "url", None)
    if url:
        return str(url)
    return None


def main():
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("Error: REPLICATE_API_TOKEN is not set.")
        return 1

    ANIMATIONS_DIR.mkdir(parents=True, exist_ok=True)

    for figure in FIGURES:
        image_path = ROOT_DIR / figure["image"]
        if not image_path.exists():
            print(f"Skipping {figure['name']}: missing {figure['image']}.")
            continue

        print(f"Generating {figure['name']} animation...")
        output = generate_animation(image_path, figure["prompt"])
        output_url = _resolve_output_url(output)
        if not output_url:
            print(f"No output URL returned for {figure['name']}.")
            continue

        output_path = ANIMATIONS_DIR / f"{figure['name']}.mp4"
        urllib.request.urlretrieve(output_url, output_path)
        print(f"Saved {figure['name']} to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
