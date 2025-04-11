import json
from typing import Dict, Tuple
import os
import gradio as gr
import torch.cuda
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorDevice, TesseractCliOcrOptions, \
    EasyOcrOptions, TesseractOcrOptions, RapidOcrOptions, OcrMacOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types import DoclingDocument
from docling.utils import model_downloader
from docling.datamodel.pipeline_options import smolvlm_picture_description

# Download models upon HF space initialization
pipeline_options = PdfPipelineOptions()
if torch.cuda.is_available():
    print("Enabling CUDA Accelerator")
    pipeline_options.accelerator_options.device = AcceleratorDevice.CUDA
    pipeline_options.accelerator_options.cuda_use_flash_attention2 = True
if os.getenv("IS_HF_SPACE"):
    print("Downloading models...")
    model_downloader.download_models()

engines_available = {
    "EasyOCR (Default)": EasyOcrOptions(),
    "Tesseract": TesseractOcrOptions(),
    "RapidOCR": RapidOcrOptions(),
    "OcrMac (Mac only)": OcrMacOptions()
}


def parse_document(
    file_path: str,
    engine: str,
    do_code_enrichment: bool,
    do_formula_enrichment: bool,
    do_picture_classification: bool,
    do_picture_description: bool,
) -> Tuple[DoclingDocument, str]:
    yield None, f"Parsing document... ⏳"

    pipeline_options.ocr_options = engines_available[engine]

    pipeline_options.do_code_enrichment = do_code_enrichment
    pipeline_options.do_formula_enrichment = do_formula_enrichment
    pipeline_options.generate_picture_images = do_picture_classification
    pipeline_options.images_scale = 2
    pipeline_options.do_picture_classification = do_picture_classification

    pipeline_options.do_picture_description = do_picture_description
    pipeline_options.picture_description_options = smolvlm_picture_description
    pipeline_options.picture_description_options.prompt = "Describe the image in three sentences. Be concise and accurate."
    pipeline_options.images_scale = 2.0
    pipeline_options.generate_picture_images = True

    print(f"Pipeline options defined: \n\t{pipeline_options}")
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(file_path)

    yield result.document, "Done ✅"


def to_html(docling_doc: DoclingDocument) -> Tuple[str, str]:
    return docling_doc.export_to_html(), "html"


def to_markdown(docling_doc: DoclingDocument) -> Tuple[str, str]:
    return docling_doc.export_to_markdown(), "md"


def to_json(docling_doc: DoclingDocument) -> Tuple[Dict, str]:
    return docling_doc.export_to_dict(), "json"


def to_text(docling_doc: DoclingDocument) -> Tuple[str, str]:
    return docling_doc.export_to_text(), "txt"

def download_file(doc: str | Dict, file_extension: str):
    # TODO: not save locally, but download through gradio!
    if file_extension == "json":
        with open('doc.json', 'w') as json_file:
            json.dump(doc, json_file, indent=4)
    else:
        with open(f"doc.{file_extension}", "w") as file:
            file.write(doc)
    return "Downloaded ✅"

def upload_file(file) -> str:
    return file.name


def setup_gradio_demo():
    with gr.Blocks() as demo:
        gr.Markdown(
            """ # Docling - OCR: Parse documents, images, spreadsheets and more to markdown or other formats!
            
            Docling is very powerful tool, with lots of cool features and integrations to other AI frameworks (e.g. LlamaIndex, LangChain, and many more).

            Model used for picture classification: [EfficientNet-B0 Document Image Classifier](https://huggingface.co/ds4sd/DocumentFigureClassifier)

            Model used for picture description: [SmolVLM-256M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct)

            To explore the full set of features of Docling visit: https://github.com/docling-project/docling
            """
        )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 1) Upload")
                file_output = gr.File(
                    file_count="single",
                    file_types=[
                        ".pdf",
                        ".docx",
                        ".pptx",
                        ".csv",
                        ".md",
                        ".png",
                        ".jpg",
                        ".tiff",
                        ".bmp",
                        ".html",
                        ".xhtml",
                        ".xlsx",
                    ],
                )

            with gr.Column():
                gr.Markdown("### 2) Configure engine & Parse")

                ocr_engine = gr.Dropdown(choices=list(engines_available.keys()), label="Select OCR engine")

                code_understanding = gr.Checkbox(
                    value=False, label="Enable Code understanding"
                )
                formula_enrichment = gr.Checkbox(
                    value=False, label="Enable Formula understanding"
                )
                picture_classification = gr.Checkbox(
                    value=False, label="Enable Picture classification"
                )
                picture_description = gr.Checkbox(
                    value=False, label="Enable Picture description"
                )
                gr.Markdown(
                    "_**Warning:** Enabling any of these features can potentially increase the processing time._"
                )

                parse_button = gr.Button("Parse document")
                status = gr.Markdown()
            with gr.Column():
                gr.Markdown("### 3) Convert")

                html_button = gr.Button("Convert to HTML")
                markdown_button = gr.Button("Convert to markdown")
                json_button = gr.Button("Convert to JSON")
                text_button = gr.Button("Convert to text")
                file_extension = gr.Text(visible=False)

        doc = gr.State()
        output = gr.Text(label="Output")

        download_button = gr.DownloadButton("Download to file")
        download_status = gr.Markdown()

        parse_button.click(
            fn=parse_document,
            inputs=[
                file_output,
                ocr_engine,
                code_understanding,
                formula_enrichment,
                picture_classification,
                picture_description,
            ],
            outputs=[doc, status],
        )
        html_button.click(
            fn=to_html,
            inputs=doc,
            outputs=[output, file_extension],
        )
        markdown_button.click(
            fn=to_markdown,
            inputs=doc,
            outputs=[output, file_extension],
        )
        json_button.click(
            fn=to_json,
            inputs=doc,
            outputs=[output, file_extension],
        )
        text_button.click(
            fn=to_text,
            inputs=doc,
            outputs=[output, file_extension],
        )
        download_button.click(
            fn=download_file,
            inputs=[output, file_extension],
            outputs=download_status,
        )
    demo.launch()


if __name__ == "__main__":
    setup_gradio_demo()
