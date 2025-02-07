import gradio as gr
import whisper
import time
from fpdf import FPDF
from docx import Document

# Load Whisper model
model = whisper.load_model("base")

# Supported languages (top 20 most spoken languages)
languages = {
    "English": "en", "Mandarin Chinese": "zh", "Hindi": "hi", "Spanish": "es", "French": "fr",
    "Arabic": "ar", "Bengali": "bn", "Russian": "ru", "Portuguese": "pt", "Urdu": "ur",
    "Indonesian": "id", "German": "de", "Japanese": "ja", "Swahili": "sw", "Marathi": "mr",
    "Telugu": "te", "Turkish": "tr", "Korean": "ko", "Tamil": "ta", "Italian": "it"
}

# Transcription function
def transcribe_audio(audio, lang):
    try:
        time.sleep(1)  # Simulate loading
        result = model.transcribe(audio, language=languages[lang])
        text = "\n".join([sentence.strip() for sentence in result["text"].split('.') if sentence])
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf_path = f"transcription_{time.strftime('%Y%m%d-%H%M%S')}.pdf"
        pdf.output(pdf_path)
        
        # Create Word document
        doc = Document()
        doc.add_paragraph(text)
        doc_path = f"transcription_{time.strftime('%Y%m%d-%H%M%S')}.docx"
        doc.save(doc_path)
        
        return text, pdf_path, doc_path
    except Exception as e:
        return f"Error: {str(e)}", None, None

# Custom CSS for professional design
custom_css = """
    body { font-family: Arial, sans-serif; background-color: #F5F5F5; color: #333333; }
    .header { background-color: #007BFF; color: white; padding: 20px; text-align: center; }
    .footer { background-color: #007BFF; color: white; padding: 10px; text-align: center; }
    .textbox textarea { color: #007BFF !important; font-size: 14px; }
    .download-buttons { margin-top: 20px; }
"""

# Gradio UI with professional design
with gr.Blocks(css=custom_css) as demo:
    # Header
    gr.Markdown("""
    <div class="header">
        <h1>VoiceHub by veltoIA</h1>
        <p>Capture audio from anywhere, pull the insights that matter, and protect your content all in one place.</p>
    </div>
    """)

    # Main content
    with gr.Row():
        audio_input = gr.Audio(label="Upload Audio or Video", type="filepath")
        lang_select = gr.Dropdown(choices=list(languages.keys()), label="Select Language", value="English")
    
    text_output = gr.Textbox(label="Transcribed Text", lines=10, interactive=False)
    
    # Download buttons (initially hidden)
    with gr.Row(visible=False) as download_row:
        download_pdf = gr.File(label="Download as PDF")
        download_docx = gr.File(label="Download as Word")
    
    # Process audio input
    audio_input.change(
        transcribe_audio,
        inputs=[audio_input, lang_select],
        outputs=[text_output, download_pdf, download_docx],
        show_progress=True
    ).then(lambda: gr.update(visible=True), None, download_row)

    # Footer
    gr.Markdown("""
    <div class="footer">
        <p>VOICEHUB WORKS WHERE YOU WORK</p>
        <p>© 2023 VoiceHub. All rights reserved.</p>
    </div>
    """)

# Launch app
demo.launch()
