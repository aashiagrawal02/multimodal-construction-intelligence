"""Construction visualisation via Pollinations (Flux). Returns an image URL; no key required."""
from urllib.parse import quote

from .. import config


def build_image_url(description: str, style: str, width: int, height: int, seed: int | None) -> tuple[str, str]:
    prompt = f"{description}, {style}, high detail, natural lighting"
    params = f"?model={config.POLLINATIONS_MODEL}&width={width}&height={height}&nologo=true"
    if seed is not None:
        params += f"&seed={seed}"
    return f"{config.POLLINATIONS_BASE_URL}/{quote(prompt)}{params}", prompt
