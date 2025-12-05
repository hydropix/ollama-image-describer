# ollama-image-describer

CLI tool to automatically generate text descriptions (captions) for images using Ollama vision models (LLaVA, Qwen3-VL, Llama Vision).

## Use Case

**Perfect for AI image generation training!** This tool is designed to help you create caption files for training LoRA (Low-Rank Adaptation) models on image generation AI like Stable Diffusion, Flux, z-image, or other diffusion models.

When training a LoRA, each image in your dataset needs an accompanying `.txt` file with a description. This tool automates that process by:
- Analyzing each image with a vision AI model
- Generating detailed, consistent descriptions
- Saving them as `.txt` files alongside your images
- Optionally adding a suffix (like artist name or style trigger word)

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** - Python package manager
- **[Ollama](https://ollama.com/)** - Must be installed separately and running

### Installing Ollama

Download and install Ollama from [ollama.com](https://ollama.com/), then pull a vision model:

```bash
ollama pull qwen3-vl:8b
```

## Installation

```bash
# Clone the repository
git clone https://github.com/hydropix/ollama-image-describer.git
cd ollama-image-describer

# Install Python dependencies with uv
uv sync
```

> **Note:** `uv sync` installs the Python dependencies (including the `ollama` Python client library). The Ollama server itself must be installed separately as described above.

## Configuration

### Environment Variables (.env)

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Configure your Ollama server:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3-vl:8b
```

### Prompt Configuration (config.yaml)

The `config.yaml` file contains:
- `system_prompt`: Instructions for the vision model
- `temperature`: Generation temperature (0.0-1.0)
- `supported_extensions`: List of image formats to process

## Usage

```bash
uv run python -m image_describer <image_folder> [options]
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--config` | `-c` | Path to YAML config file |
| `--suffix` | `-s` | Text appended to each description (e.g., ", By Artist") |
| `--overwrite/--no-overwrite` | | Overwrite existing .txt files (default: overwrite) |
| `--verbose` | `-v` | Verbose mode |

### Examples

```bash
# Basic usage
uv run python -m image_describer ./my_images

# With custom suffix
uv run python -m image_describer ./my_images --suffix ", By Kristof"

# Verbose mode with custom config
uv run python -m image_describer ./my_images -v -c custom_config.yaml
```

## Supported Models

- **Qwen3-VL** (recommended): `qwen3-vl:8b`
- **LLaVA**: `llava`, `llava:13b`
- **Llama Vision**: `llama3.2-vision`

## License

MIT
