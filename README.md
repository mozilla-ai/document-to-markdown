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
[![Docling](https://img.shields.io/badge/Docling-📝-orange)](https://github.com/docling-project/docling)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr) <br>
[![Try on Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Try%20on-Spaces-blue)](https://huggingface.co/spaces/mozilla-ai/document-to-markdown)

[Blueprints Hub](https://blueprints.mozilla.ai/)
| [Contributing](CONTRIBUTING.md)

🤝 **_This Blueprint was a result of an [EleutherAI](https://www.eleuther.ai/) <> [mozilla.ai](https://www.mozilla.ai/) collaboration, as part of their work on [Open Datasets for LLM Training](https://blog.mozilla.org/en/mozilla/dataset-convening/)_**.

**_The tools & methods showcased in this blueprint were also part of EleutherAI's work on the [Common Pile 0.1](https://huggingface.co/collections/common-pile/common-pile-v01-68307d37df48e36f02717f21)_**.

</div>

# Parse and convert Documents with [Docling](https://github.com/docling-project/docling)

This blueprint guides you to convert various unstructured documents (PDFs, DOCX, HTML, etc.) to markdown, or other, formats using the Docling CLI or a locally-hosted demo UI, with special attention to OCR capabilities and image handling options.

## Table of Contents

- [Quick-start](#quick-start)
- [How it Works](#how-it-works)
- [Features & Configuration](#features--configuration)
- [Hardware requirements](#hardware-requirements)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contributing](#contributing)

## Quick-start

We have built a simple Graphical Interface demo of Docling to showcase some basic functionality. To utilize the full set of features, see section [Local CLI for the full Docling experience!](#local-cli-for-the-full-docling-experience) You can try the demo in two ways:

### HF Spaces Demo 

[![Try on Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Try%20on-Spaces-blue)](https://huggingface.co/spaces/mozilla-ai/document-to-markdown)

### Local Demo

You can also run the demo locally. First, clone the repository:

```bash
git clone https://github.com/mozilla-ai/document-to-markdown.git
```

Then, navigate to the directory, create a virtual environment and install the requirements:

```bash
cd document-to-markdown/demo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Finally, run the demo:

```bash
python app.py
```
This will start a local server, and you can access the demo at `http://127.0.0.1:7860`.

### Local CLI for the full Docling experience! 

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

## How it Works

Docling is a document processing tool that parses various formats and provides a unified representation. The CLI simplifies access to its features:

1. **Document Parsing**: Docling parses your document and extracts text, tables, images, and structure
2. **Layout Analysis**: For PDFs, it analyzes page layout to determine reading order
3. **OCR Processing**: For scanned documents, it applies OCR to extract text
4. **Markdown Conversion**: The parsed document is converted to Markdown format
5. **Image Handling**: Images can be embedded, referenced, or replaced with placeholders

## Features & Configuration

**Note: These are only a few samples of the full set of features of Docling!** Visit https://github.com/docling-project/docling for an up-to-date list of all the features and configurations.

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

### Parse Images with SmolDocling

Using the VLM Pipeline, we can use a Vision Language Model with [SmolDocling](https://huggingface.co/ds4sd/SmolDocling-256M-preview) to describe images:

```bash
docling path/to/document.pdf --pipeline vlm --vlm-model smoldocling
```

We can also use [EfficientNet-B0 Document Image Classifier](https://huggingface.co/ds4sd/DocumentFigureClassifier) to classify images:

```bash
docling path/to/document.pdf --enrich-picture-classes
```


### Parse Code 

```bash
docling path/to/document.pdf --enrich-code
```

### Parse Formulas 

```bash
docling path/to/document.pdf --enrich-formula
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


## Hardware requirements:
  - OS: Windows, macOS, or Linux
  - Python 3.10 or higher
  - Minimum RAM: 8GB
  - Disk space: 4GB for models and dependencies
  - GPU: optional

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
