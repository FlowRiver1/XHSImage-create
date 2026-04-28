#!/usr/bin/env python3
"""
Generate a Xiaohongshu cover image with OpenAI or Gemini image APIs.

Usage examples:
  # OpenAI (image2.0 alias -> gpt-image-1)
  python scripts/generate_image2_cover.py --provider openai --model image2.0 --prompt-file outputs/prompt.txt --output outputs/cover_openai.png

  # Gemini (Nano Banana alias -> gemini-2.5-flash-image)
  python scripts/generate_image2_cover.py --provider gemini --model nanobanana --prompt-file outputs/prompt.txt --output outputs/cover_gemini.png
"""

import argparse
import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request


OPENAI_MODEL_ALIASES = {
    "image2": "gpt-image-1",
    "image2.0": "gpt-image-1",
    "gpt-image2": "gpt-image-1",
    "chatgpt-image2": "gpt-image-1",
}

GEMINI_MODEL_ALIASES = {
    "nanobanana": "gemini-2.5-flash-image",
    "nano-banana": "gemini-2.5-flash-image",
    "nano banana": "gemini-2.5-flash-image",
    "nanobanana2": "gemini-3.1-flash-image-preview",
    "nano-banana-2": "gemini-3.1-flash-image-preview",
    "nano banana 2": "gemini-3.1-flash-image-preview",
    "nanobanana-pro": "gemini-3-pro-image-preview",
    "nano-banana-pro": "gemini-3-pro-image-preview",
    "nano banana pro": "gemini-3-pro-image-preview",
}


def normalize_model(provider: str, model: str) -> str:
    lowered = model.strip().lower()
    if provider == "openai":
        return OPENAI_MODEL_ALIASES.get(lowered, model.strip())
    return GEMINI_MODEL_ALIASES.get(lowered, model.strip())


def load_prompt(args: argparse.Namespace) -> str:
    prompt = args.prompt or ""
    if args.prompt_file:
        prompt = pathlib.Path(args.prompt_file).read_text(encoding="utf-8")
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("Prompt is empty. Use --prompt or --prompt-file.")
    return prompt


def ensure_parent_dir(path: pathlib.Path) -> None:
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def request_openai_image(
    api_key: str,
    api_base: str,
    model: str,
    prompt: str,
    size: str,
    n: int,
) -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": n,
    }
    body = json.dumps(payload).encode("utf-8")
    url = api_base.rstrip("/") + "/images/generations"
    req = urllib.request.Request(
        url=url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def extract_openai_image_bytes(response_json: dict) -> bytes:
    data = response_json.get("data")
    if not isinstance(data, list) or not data:
        raise ValueError("No image data returned by API.")

    first = data[0] or {}
    b64_value = first.get("b64_json")
    if not b64_value:
        raise ValueError("API response does not contain b64_json.")
    return base64.b64decode(b64_value)


def request_gemini_image(
    api_key: str,
    api_base: str,
    model: str,
    prompt: str,
    aspect_ratio: str,
    image_size: str,
) -> dict:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect_ratio},
        },
    }
    if image_size:
        payload["generationConfig"]["imageConfig"]["imageSize"] = image_size

    body = json.dumps(payload).encode("utf-8")
    url = api_base.rstrip("/") + f"/models/{model}:generateContent"
    req = urllib.request.Request(
        url=url,
        data=body,
        method="POST",
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def extract_gemini_image_bytes(response_json: dict) -> bytes:
    candidates = response_json.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("No candidates returned by Gemini API.")

    content = (candidates[0] or {}).get("content") or {}
    parts = content.get("parts")
    if not isinstance(parts, list) or not parts:
        raise ValueError("No parts returned by Gemini API.")

    for part in parts:
        inline_data = part.get("inlineData") or part.get("inline_data")
        if isinstance(inline_data, dict):
            data = inline_data.get("data")
            if data:
                return base64.b64decode(data)
    raise ValueError("Gemini API response does not contain inline image data.")


def resolve_api_key(provider: str, explicit_api_key: str) -> str:
    if explicit_api_key:
        return explicit_api_key.strip()
    env_name = "OPENAI_API_KEY" if provider == "openai" else "GEMINI_API_KEY"
    return os.getenv(env_name, "").strip()


def resolve_api_base(provider: str, explicit_api_base: str) -> str:
    if explicit_api_base:
        return explicit_api_base.strip()
    if provider == "openai":
        return "https://api.openai.com/v1"
    return "https://generativelanguage.googleapis.com/v1beta"


def default_model_for(provider: str) -> str:
    if provider == "openai":
        return "gpt-image-1"
    return "gemini-2.5-flash-image"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate cover image with OpenAI or Gemini image model.",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "gemini"],
        default="openai",
        help="Image provider",
    )
    parser.add_argument("--prompt", help="Prompt text for image generation")
    parser.add_argument(
        "--prompt-file",
        help="UTF-8 text file containing prompt",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output image path, e.g. outputs/cover.png",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Model name. OpenAI aliases: image2,image2.0. Gemini aliases: nanobanana,nanobanana2,nanobanana-pro",
    )
    parser.add_argument(
        "--size",
        default="1024x1536",
        help="OpenAI image size, e.g. 1024x1536",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="OpenAI number of images (keep 1 for deterministic workflow)",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="3:4",
        help="Gemini aspect ratio, e.g. 3:4 / 9:16 / 1:1",
    )
    parser.add_argument(
        "--image-size",
        default="",
        help="Gemini image size for 3.x preview models, e.g. 1K/2K/4K",
    )
    parser.add_argument(
        "--api-base",
        default="",
        help="Custom API base URL (optional)",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="API key override. If empty, uses OPENAI_API_KEY or GEMINI_API_KEY by provider",
    )
    parser.add_argument(
        "--save-response",
        action="store_true",
        help="Save full API JSON next to output image",
    )
    args = parser.parse_args()

    try:
        prompt = load_prompt(args)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    provider = args.provider
    model = args.model.strip() if args.model.strip() else default_model_for(provider)
    model = normalize_model(provider, model)
    api_key = resolve_api_key(provider, args.api_key)
    api_base = resolve_api_base(provider, args.api_base)

    if not api_key:
        missing = "OPENAI_API_KEY" if provider == "openai" else "GEMINI_API_KEY"
        print(f"[ERROR] {missing} is not set.")
        return 1

    output_path = pathlib.Path(args.output).resolve()
    ensure_parent_dir(output_path)

    try:
        if provider == "openai":
            response_json = request_openai_image(
                api_key=api_key,
                api_base=api_base,
                model=model,
                prompt=prompt,
                size=args.size,
                n=args.n,
            )
            image_bytes = extract_openai_image_bytes(response_json)
        else:
            response_json = request_gemini_image(
                api_key=api_key,
                api_base=api_base,
                model=model,
                prompt=prompt,
                aspect_ratio=args.aspect_ratio,
                image_size=args.image_size,
            )
            image_bytes = extract_gemini_image_bytes(response_json)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        print(f"[ERROR] HTTP {exc.code}: {detail}")
        return 1
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    output_path.write_bytes(image_bytes)
    print(f"[OK] Image generated ({provider}/{model}): {output_path}")

    if args.save_response:
        json_path = output_path.with_suffix(".json")
        json_path.write_text(
            json.dumps(response_json, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[OK] API response saved: {json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
