<p align="center">
  <picture>
    <!-- When the user prefers dark mode, show the white logo -->
    <source media="(prefers-color-scheme: dark)" srcset="./images/Blueprint-logo-white.png">
    <!-- When the user prefers light mode, show the black logo -->
    <source media="(prefers-color-scheme: light)" srcset="./images/Blueprint-logo-black.png">
    <!-- Fallback: default to the black logo -->
    <img src="./images/Blueprint-logo-black.png" width="35%" alt="Project logo"/>
  </picture>
</p>


<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr) <br>
[![Docs](https://github.com/mozilla-ai/blueprint-template/actions/workflows/docs.yaml/badge.svg)](https://github.com/mozilla-ai/blueprint-template/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/blueprint-template/actions/workflows/tests.yaml/badge.svg)](https://github.com/mozilla-ai/blueprint-template/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/blueprint-template/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/blueprint-template/actions/workflows/lint.yaml/)

[Blueprints Hub](https://developer-hub.mozilla.ai/)
| [Documentation](https://mozilla-ai.github.io/Blueprint-template/)
| [Getting Started](https://mozilla-ai.github.io/Blueprint-template/getting-started)
| [Contributing](CONTRIBUTING.md)

</div>

# Converting Documents to Markdown with Docling CLI

This blueprint guides you to convert various unstructured documents (PDFs, DOCX, HTML, etc.) to Markdown format using the Docling command-line interface, with special attention to OCR capabilities and image handling options.

## Pre-requisites

- **System requirements**:
  - OS: Windows, macOS, or Linux
  - Python 3.10 or higher
  - Minimum RAM: 8GB
  - Disk space: 4GB for models and dependencies
  - GPU: optional

- **Dependencies**:
  - All Python dependencies are installed automatically with Docling

## Quick-start

Install Docling using pip:

```bash
pip install docling
```

Basic usage to convert a PDF to Markdown:

```bash
# Convert a local file
docling path/to/document.pdf

# Convert from a URL
docling https://arxiv.org/pdf/2408.09869
```

For advanced OCR with multiple languages:

```bash
docling path/to/document.pdf --ocr-lang en,fr,de
```

To use the SmolDocling Vision Language Model (VLM) pipeline:

```bash
docling path/to/document.pdf --pipeline vlm --vlm-model smoldocling
```

## How it Works

Docling is a document processing tool that parses various formats and provides a unified representation. The CLI simplifies access to its features:

1. **Document Parsing**: Docling parses your document and extracts text, tables, images, and structure
2. **Layout Analysis**: For PDFs, it analyzes page layout to determine reading order
3. **OCR Processing**: For scanned documents, it applies OCR to extract text
4. **Markdown Conversion**: The parsed document is converted to Markdown format
5. **Image Handling**: Images can be embedded, referenced, or replaced with placeholders

### OCR Options

Docling supports multiple OCR engines:

#### EasyOCR (Default)

```bash
# Specify languages
docling path/to/document.pdf --ocr-lang en,fr,de

# Disable OCR entirely
docling path/to/document.pdf --no-ocr
```

#### Tesseract OCR

```bash
docling path/to/document.pdf --ocr-engine tesseract
```

#### RapidOCR

```bash
# Install RapidOCR first
pip install rapidocr_onnxruntime

# Then use it with Docling
docling path/to/document.pdf --ocr-engine rapidocr
```

#### OcrMac (macOS only)

```bash
# Install OcrMac first
pip install ocrmac

# Then use it with Docling
docling path/to/document.pdf --ocr-engine ocrmac
```

### VLM Pipeline with SmolDocling

For complex documents, the Vision Language Model pipeline with [SmolDocling](https://huggingface.co/ds4sd/SmolDocling-256M-preview) can provide better results:

```bash
docling path/to/document.pdf --pipeline vlm --vlm-model smoldocling
```

On Apple Silicon Macs, this automatically uses MLX acceleration for better performance.

### Image Embedding Options

Control how images appear in your Markdown output:

#### Embedded Images (Data URLs)

```bash
docling path/to/document.pdf --image-mode embedded
```

Embeds images directly in the Markdown file using Base64 encoding, creating a self-contained document.

#### Referenced Images (Default)

```bash
docling path/to/document.pdf --image-mode referenced
```

Saves images as separate files and references them using relative paths in the Markdown.

#### Placeholder Images

```bash
docling path/to/document.pdf --image-mode placeholder
```

Replaces images with placeholder text in the Markdown.

### Batch Processing

Convert multiple files at once:

```bash
docling ./documents/ --from pdf --to md --output ./markdown_files
```

## Troubleshooting

### OCR Issues

If you encounter OCR problems:

```bash
# Try a different OCR engine
docling path/to/document.pdf --ocr-engine tesseract

# Force OCR on the entire page
docling path/to/document.pdf --force-full-page-ocr
```

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.