"""Processor for handling images in a folder."""

from pathlib import Path

from .config import Config
from .ollama_client import describe_image


def find_images(folder: Path, extensions: list[str]) -> list[Path]:
    """Find all images in a folder.

    Args:
        folder: Folder to scan.
        extensions: List of supported extensions.

    Returns:
        List of paths to found images.
    """
    images = set()
    for ext in extensions:
        images.update(folder.glob(f"*{ext}"))
        images.update(folder.glob(f"*{ext.upper()}"))
    return sorted(images)


def process_images(
    folder: Path,
    config: Config,
    overwrite: bool = False,
    verbose: bool = False,
) -> tuple[int, int]:
    """Process all images in a folder.

    Args:
        folder: Folder containing images.
        config: Application configuration.
        overwrite: If True, overwrite existing .txt files.
        verbose: If True, display detailed information.

    Returns:
        Tuple (number of images processed, number of images skipped).
    """
    images = find_images(folder, config.supported_extensions)
    processed = 0
    skipped = 0

    total = len(images)
    if verbose:
        print(f"Found {total} image(s) to process.")

    for i, image_path in enumerate(images, 1):
        txt_path = image_path.with_suffix(".txt")

        if txt_path.exists() and not overwrite:
            if verbose:
                print(f"[{i}/{total}] Skipped (already exists): {image_path.name}")
            skipped += 1
            continue

        print(f"[{i}/{total}] Processing: {image_path.name}...")

        try:
            description = describe_image(
                image_path=image_path,
                model=config.model,
                system_prompt=config.system_prompt,
                temperature=config.temperature,
                ollama_host=config.ollama_host,
            )

            if config.description_suffix:
                description = description + config.description_suffix

            txt_path.write_text(description, encoding="utf-8")
            processed += 1

            if verbose:
                print(f"  -> Saved: {txt_path.name}")

        except Exception as e:
            print(f"  Error: {e}")
            skipped += 1

    return processed, skipped
