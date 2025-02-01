import gradio as gr
import numpy as np
from docx import Document
import uuid
import os
import logging
import soundfile as sf

from engine.stt import STT

logging.basicConfig(level=logging.INFO)


class Driver:
    def __init__(self):
        self.stt = STT()
        self.transcriptions = []
        self.audios_dir_path = "data/audios/"
        self.transcriptions_dir_path = "data/transcriptions/"

        # create directories if not exist
        os.makedirs(self.audios_dir_path, exist_ok=True)
        os.makedirs(self.transcriptions_dir_path, exist_ok=True)

    
    def transcribe(self, audio):
        if audio is None:
            return self.show_all_transcriptions()
        
        sr, y = self.__process_audio__(audio)

        audio_path = os.path.join(self.audios_dir_path, f"{uuid.uuid4()}.wav")
        sf.write(audio_path, y, sr)

        transcription = self.stt.transcribe(audio_path)

        if transcription is None:
            return self.show_all_transcriptions()

        logging.info(f"Transcription: {transcription}")

        self.transcriptions.append(transcription)
        
        return self.show_all_transcriptions()


    def delete_last_transcription(self):
        if len(self.transcriptions) > 0:
            self.transcriptions.pop()

    def __process_audio__(self, audio):
        sr, y = audio
        # Convert to mono if stereo
        if y.ndim > 1:
            y = y.mean(axis=1)
        
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))

        return sr, y


    def show_all_transcriptions(self):
        return "\n".join(self.transcriptions)
    

    def delete_all_transcriptions(self):
        self.transcriptions = []


    def save_transcriptions_to_file(self, filename):
        if filename == "":
            # generate a uuid
            filename = str(uuid.uuid4())
        
        doc = Document()

        for transcription in self.transcriptions:
            doc.add_paragraph(transcription)
        
        # save to docx
        doc_path = os.path.join(self.transcriptions_dir_path, filename + ".docx")
        doc.save(doc_path)
        
        # save to txt
        txt_path = os.path.join(self.transcriptions_dir_path, filename + ".txt")
        with open(txt_path, "w") as txt_file:
            for transcription in self.transcriptions:
                txt_file.write(transcription + "\n")
        
        return [doc_path, txt_path]


# Create a Gradio interface with a button to clear transcriptions
with gr.Blocks() as demo:
    driver = Driver()

    audio_input = gr.Audio(sources="microphone")
    text_output = gr.Textbox(label="Transcription")

    delete_last_line_button = gr.Button("Delete Last Line")

    audio_input.change(fn=driver.transcribe, inputs=audio_input, outputs=text_output)
    
    delete_last_line_button.click(fn=driver.delete_last_transcription, inputs=None, outputs=text_output)
    
    
    delete_all_lines_button = gr.Button("Delete All Lines")
    delete_all_lines_button.click(fn=driver.delete_all_transcriptions, inputs=None, outputs=text_output)


    filename_input = gr.Textbox(label="Mention a filename to save the transcriptions")
    # Add a file output component for downloading
    file_output = gr.File(
        label="Download Transcriptions", 
        file_count="multiple", 
        type="filepath",
        file_types=["docx", "txt"]
    )

    save_button = gr.Button("Save & Generate Download Links")

    save_button.click(fn=driver.save_transcriptions_to_file, inputs=filename_input, outputs=file_output)

demo.launch(share=True, server_name="0.0.0.0", server_port=8080)
