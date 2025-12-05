"""Client pour l'API Ollama avec support des modèles de vision."""

import base64
from pathlib import Path

from ollama import Client


def encode_image_base64(image_path: Path) -> str:
    """Encode une image en base64.

    Args:
        image_path: Chemin vers l'image.

    Returns:
        L'image encodée en base64.
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def describe_image(
    image_path: Path,
    model: str,
    system_prompt: str,
    temperature: float = 0.7,
    ollama_host: str | None = None,
) -> str:
    """Génère une description d'une image via Ollama.

    Args:
        image_path: Chemin vers l'image à décrire.
        model: Nom du modèle Ollama à utiliser.
        system_prompt: Prompt système pour guider la description.
        temperature: Température pour la génération.
        ollama_host: URL du serveur Ollama (optionnel).

    Returns:
        La description générée par le modèle.

    Raises:
        ollama.ResponseError: En cas d'erreur de l'API Ollama.
    """
    image_data = encode_image_base64(image_path)

    client = Client(host=ollama_host) if ollama_host else Client()

    response = client.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": system_prompt,
                "images": [image_data],
            }
        ],
        options={"temperature": temperature},
    )

    return response["message"]["content"]
