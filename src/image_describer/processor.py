"""Processeur pour traiter les images d'un dossier."""

from pathlib import Path

from .config import Config
from .ollama_client import describe_image


def find_images(folder: Path, extensions: list[str]) -> list[Path]:
    """Trouve toutes les images dans un dossier.

    Args:
        folder: Dossier à scanner.
        extensions: Liste des extensions supportées.

    Returns:
        Liste des chemins vers les images trouvées.
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
    """Traite toutes les images d'un dossier.

    Args:
        folder: Dossier contenant les images.
        config: Configuration de l'application.
        overwrite: Si True, écrase les fichiers .txt existants.
        verbose: Si True, affiche des informations détaillées.

    Returns:
        Tuple (nombre d'images traitées, nombre d'images ignorées).
    """
    images = find_images(folder, config.supported_extensions)
    processed = 0
    skipped = 0

    total = len(images)
    if verbose:
        print(f"Trouvé {total} image(s) à traiter.")

    for i, image_path in enumerate(images, 1):
        txt_path = image_path.with_suffix(".txt")

        if txt_path.exists() and not overwrite:
            if verbose:
                print(f"[{i}/{total}] Ignoré (existe déjà): {image_path.name}")
            skipped += 1
            continue

        print(f"[{i}/{total}] Traitement: {image_path.name}...")

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
                print(f"  -> Sauvegardé: {txt_path.name}")

        except Exception as e:
            print(f"  Erreur: {e}")
            skipped += 1

    return processed, skipped
