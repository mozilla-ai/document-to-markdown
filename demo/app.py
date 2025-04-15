import json
from typing import Dict, Tuple
import os
import gradio as gr
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    EasyOcrOptions,
    TesseractOcrOptions,
    RapidOcrOptions,
    OcrMacOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types import DoclingDocument
from docling.utils import model_downloader

# Download models upon HF space initialization
if os.getenv("IS_HF_SPACE"):
    print("Downloading models...")
    model_downloader.download_models()

engines_available = {
    "EasyOCR (Default)": EasyOcrOptions(),
    "Tesseract": TesseractOcrOptions(),
    "RapidOCR": RapidOcrOptions(),
    "OcrMac (Mac only)": OcrMacOptions(),
}


def parse_document(
    file_path: str,
    engine: str,
    do_code_enrichment: bool,
    do_formula_enrichment: bool,
) -> Tuple[DoclingDocument, str]:
    yield None, f"Parsing document... ⏳"

    pdf_pipeline_options = PdfPipelineOptions()
    pdf_pipeline_options.ocr_options = engines_available[engine]
    pdf_pipeline_options.do_code_enrichment = do_code_enrichment
    pdf_pipeline_options.do_formula_enrichment = do_formula_enrichment

    print(f"PDF Pipeline options defined: \n\t{pdf_pipeline_options}")
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options)
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
    final_filename = f"doc.{file_extension}"
    if file_extension == "json":
        with open(final_filename, "w") as json_file:
            json.dump(doc, json_file, indent=4)
    else:
        with open(final_filename, "w") as file:
            file.write(doc)
    return [final_filename, "Downloaded ✅"]


def upload_file(file) -> str:
    return file.name


def setup_gradio_demo():
    with gr.Blocks() as demo:
        gr.Markdown(
            """ # Docling - OCR: Parse documents, images, spreadsheets and more to markdown or other formats!
            
            Docling is very powerful tool, with lots of cool features and integrations to other AI frameworks (e.g. LlamaIndex, LangChain, and many more).

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
                gr.Markdown("### 2) Configure engine (Only applicable for PDF files)")

                ocr_engine = gr.Dropdown(
                    choices=list(engines_available.keys()), label="Select OCR engine"
                )

                code_understanding = gr.Checkbox(
                    value=False, label="Enable Code understanding"
                )
                formula_enrichment = gr.Checkbox(
                    value=False, label="Enable Formula understanding"
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
        with gr.Column():
            with gr.Group():
                output = gr.Textbox(
                    label="Output",
                    lines=10,
                    interactive=False,
                    elem_id="output-textbox",
                )
                gr.HTML(
                    """
                    <div style="display: flex; flex-direction: column; align-items: center;">
                      <button id="copy-button" onclick="const text = document.getElementById('output-textbox').querySelector('textarea').value; navigator.clipboard.writeText(text); const copiedMsg = document.getElementById('copied-msg'); copiedMsg.style.display = 'inline'; setTimeout(() => copiedMsg.style.display = 'none', 1500);" style="margin-top: 10px;">
                        📋 Copy output to clipboard
                      </button>
                      <span id="copied-msg" style="margin-left: 10px; color: green; display: none;">Copied!</span>
                    </div>
                    """
                )

        download_button = gr.Button("Download to file")
        # See https://github.com/gradio-app/gradio/issues/9230#issuecomment-2323771634 why this button
        download_button_hidden = gr.DownloadButton(
            visible=False, elem_id="download_btn_hidden"
        )
        download_status = gr.Markdown()

        parse_button.click(
            fn=parse_document,
            inputs=[
                file_output,
                ocr_engine,
                code_understanding,
                formula_enrichment,
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
            outputs=[download_button_hidden, download_status],
        ).then(
            fn=None,
            inputs=None,
            outputs=None,
            js="() => document.querySelector('#download_btn_hidden').click()",
        )

    demo.launch()


if __name__ == "__main__":
    setup_gradio_demo()
