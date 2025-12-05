"""Point d'entrée CLI pour l'application Image Describer."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from .config import load_config
from .processor import process_images

app = typer.Typer(
    name="image-describer",
    help="Génère des descriptions d'images avec Ollama Vision.",
)


@app.command()
def main(
    dossier_images: Annotated[
        Path,
        typer.Argument(
            help="Chemin du dossier contenant les images",
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
            help="Chemin du fichier YAML de configuration",
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
            help="Texte ajouté à la fin de chaque description (ex: ', By Artist')",
        ),
    ] = None,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite/--no-overwrite",
            help="Écraser les fichiers .txt existants (activé par défaut)",
        ),
    ] = True,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Mode verbeux",
        ),
    ] = False,
) -> None:
    """Traite les images d'un dossier et génère des descriptions."""
    cfg = load_config(config, suffix=suffix)

    if verbose:
        print(f"Modèle: {cfg.model}")
        print(f"Dossier: {dossier_images}")
        print(f"Extensions: {', '.join(cfg.supported_extensions)}")
        print("-" * 40)

    processed, skipped = process_images(
        folder=dossier_images,
        config=cfg,
        overwrite=overwrite,
        verbose=verbose,
    )

    print("-" * 40)
    print(f"Terminé! {processed} image(s) traitée(s), {skipped} ignorée(s).")


if __name__ == "__main__":
    app()
