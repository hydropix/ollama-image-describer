"""CLI entry point for the Image Describer application."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from .config import load_config
from .processor import process_images

app = typer.Typer(
    name="image-describer",
    help="Generate image descriptions with Ollama Vision.",
)


@app.command()
def main(
    image_folder: Annotated[
        Path,
        typer.Argument(
            help="Path to the folder containing images",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ],
    config: Annotated[
        Optional[Path],
        typer.Option(
            "--config",
            "-c",
            help="Path to YAML configuration file",
            exists=True,
            file_okay=True,
            dir_okay=False,
        ),
    ] = None,
    suffix: Annotated[
        Optional[str],
        typer.Option(
            "--suffix",
            "-s",
            help="Text appended to each description (e.g., ', By Artist')",
        ),
    ] = None,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite/--no-overwrite",
            help="Overwrite existing .txt files (enabled by default)",
        ),
    ] = True,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Verbose mode",
        ),
    ] = False,
) -> None:
    """Process images in a folder and generate descriptions."""
    cfg = load_config(config, suffix=suffix)

    if verbose:
        print(f"Model: {cfg.model}")
        print(f"Folder: {image_folder}")
        print(f"Extensions: {', '.join(cfg.supported_extensions)}")
        print("-" * 40)

    processed, skipped = process_images(
        folder=image_folder,
        config=cfg,
        overwrite=overwrite,
        verbose=verbose,
    )

    print("-" * 40)
    print(f"Done! {processed} image(s) processed, {skipped} skipped.")


if __name__ == "__main__":
    app()
