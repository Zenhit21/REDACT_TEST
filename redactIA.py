import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import language_tool_python
from vosk import Model, KaldiRecognizer
import wave
import json
import interface
# pip install mysql-connector-python
# ============================
# 📌 Inicializar LanguageTool (Evita múltiples instancias)
# ============================
tool = language_tool_python.LanguageTool('es')

# ============================
# 🔄 Función para corregir texto de forma eficiente
# ============================
def correct_text_handler():
    """Corrige el texto en un hilo separado para evitar congelar la UI."""
    input_text = interface.text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Aviso", "Por favor, ingresa un texto para corregir.")
        return

    # 🔒 Deshabilitar el botón mientras corrige
    interface.button_correct.config(state=tk.DISABLED)
    interface.text_output.delete("1.0", tk.END)
    interface.text_output.insert(tk.END, "Corrigiendo...")

    def process_correction():
        corrected = tool.correct(input_text)
        interface.text_output.delete("1.0", tk.END)
        interface.text_output.insert(tk.END, corrected)
        interface.button_correct.config(state=tk.NORMAL)  # 🔓 Volver a habilitar el botón

    # 🏃 Ejecutar en un hilo separado para no congelar la interfaz
    threading.Thread(target=process_correction, daemon=True).start()

# ============================
# 🎙 Transcripción con Vosk
# ============================
VOSK_MODEL_PATH = "vosk-model-es-0.42"

if not os.path.exists(VOSK_MODEL_PATH):
    messagebox.showerror("Error", "No se encontró el modelo de Vosk. Descárgalo de https://alphacephei.com/vosk/models")
    exit()

model = Model(VOSK_MODEL_PATH)

def convert_audio_to_wav(input_audio):
    """Convierte audio a WAV compatible con Vosk (16kHz mono)."""
    output_wav = "temp_audio.wav"
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_audio, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_wav],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return output_wav
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error al convertir el audio con ffmpeg.")
        return None

def transcribe_audio(audio_path):
    """Transcribe un archivo de audio con Vosk."""
    wav_path = convert_audio_to_wav(audio_path)
    if not wav_path:
        return ""

    recognizer = KaldiRecognizer(model, 16000)

    with wave.open(wav_path, "rb") as wf:
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            recognizer.AcceptWaveform(data)

    result_json = json.loads(recognizer.FinalResult())
    transcription = result_json.get("text", "").strip()
    
    os.remove(wav_path)  # Eliminar archivo temporal
    return transcription

def select_audio_file():
    """Selecciona un archivo de audio."""
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo de audio",
        filetypes=[("Archivos de audio", "*.wav *.m4a *.mp3 *.ogg *.flac")]
    )
    if file_path:
        interface.label_audio_file.config(text=file_path)

def transcribe_audio_handler():
    """Transcribe el audio seleccionado en un hilo separado."""
    audio_file = interface.label_audio_file.cget("text")
    if not audio_file or audio_file == "Ningún archivo seleccionado":
        messagebox.showwarning("Aviso", "Debes seleccionar un archivo de audio primero.")
        return

    interface.button_transcribe_audio.config(state=tk.DISABLED)
    interface.text_audio_output.delete("1.0", tk.END)
    interface.text_audio_output.insert(tk.END, "Transcribiendo...")

    def process_transcription():
        transcription = transcribe_audio(audio_file)
        interface.text_audio_output.delete("1.0", tk.END)
        interface.text_audio_output.insert(tk.END, transcription)
        interface.button_transcribe_audio.config(state=tk.NORMAL)

    threading.Thread(target=process_transcription, daemon=True).start()