import io

import pyttsx3
from tkinter import Tk, filedialog
import PyPDF4
import fitz
from pydub import AudioSegment


def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text_content = file.read()
            return text_content
    except IOError:
        print("Error: Unable to read the file.")
        return None

# def read_pdf_content(file_path):
#     try:
#         text_content = ""
#         with open(file_path, 'rb') as file:
#             pdf_reader = PyPDF4.PdfFileReader(file)
#             num_pages = pdf_reader.getNumPages()
#             for page_num in range(num_pages):
#                 page = pdf_reader.getPage(page_num)
#                 text_content += page.extractText()
#         return text_content
#     except Exception as e:
#         print("Error while reading PDF:", e)
#         return None
def read_pdf_content(file_content):
    try:
        text_content = ""
        pdf_file = io.BytesIO(file_content)
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_content += page.get_text()

        pdf_document.close()

        return text_content
    except Exception as e:
        print("Error while reading PDF:", e)
        return None
# def text_to_speech(text_content):
#     try:
#         engine = pyttsx3.init()
#         engine.say(text_content)
#         engine.runAndWait()
#     except Exception as e:
#         print("Error during text-to-speech:", e)

# def text_to_speech(text_content, output_file):
#     try:
#         engine = pyttsx3.init()
#         # voices = engine.getProperty('voices')
#         # engine.setProperty('voice', voices[voice_id].id)
#         #
#         # Save the text-to-speech output as a WAV file
#         engine.save_to_file(text_content, "output.wav")
#         engine.runAndWait()
#
#         # Convert the WAV file to MP3 using pydub
#         from pydub import AudioSegment
#         audio = AudioSegment.from_wav("output.wav")
#         audio.export(output_file, format="mp3")
#
#         # Remove the temporary WAV file
#         import os
#         os.remove("output.wav")
#     except Exception as e:
#         print("Error during text-to-speech:", e)

def text_to_speech(text_content):
    try:
        engine = pyttsx3.init()
        engine.say(text_content)
        engine.runAndWait()

        # Since pyttsx3 doesn't provide a direct way to save to a buffer,
        # we'll use a temporary file to save the audio output.
        temp_output_file = "output.wav"
        engine.save_to_file(text_content, temp_output_file)
        engine.runAndWait()

        # Convert the WAV file to MP3 using pydub
        audio = AudioSegment.from_wav(temp_output_file)

        # Export the MP3 data as bytes
        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format='mp3')

        # Remove the temporary WAV file
        import os
        os.remove(temp_output_file)

        return mp3_buffer.getvalue()  # Return the binary data of the MP3 file
    except Exception as e:
        print("Error during text-to-speech:", e)
        return None
def main():
    Tk().withdraw()  # Prevent the Tkinter window from appearing
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])

    if file_path:
        if file_path.endswith('.txt'):
            text_content = read_text_from_file(file_path)
        elif file_path.endswith('.pdf'):
            text_content = read_pdf_content(file_path)
        else:
            print("Unsupported file format.")
            return

        if text_content:
            text_to_speech(text_content)
        else:
            print("No content in the file or an error occurred while reading.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
