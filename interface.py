import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import language_tool_python
from vosk import Model, KaldiRecognizer
import wave
import json
import redactIA


root = tk.Tk()
root.title("Herramienta IA (Vosk & Corrección de Texto)")
root.geometry("600x500")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# 📌 Pestaña de Texto
frame_text = ttk.Frame(notebook)
notebook.add(frame_text, text="Texto")

label_text = ttk.Label(frame_text, text="Ingresa el texto:")
label_text.pack(pady=5)

text_input = tk.Text(frame_text, height=10, width=60)
text_input.pack(pady=5)

button_correct = ttk.Button(frame_text, text="Corregir Texto", command=redactIA.correct_text_handler)
button_correct.pack(pady=5)

label_text_output = ttk.Label(frame_text, text="Texto corregido:")
label_text_output.pack(pady=5)

text_output = tk.Text(frame_text, height=10, width=60)
text_output.pack(pady=5)

# 📌 Pestaña de Audio
frame_audio = ttk.Frame(notebook)
notebook.add(frame_audio, text="Audio")

button_select_audio = ttk.Button(frame_audio, text="Seleccionar Archivo de Audio", command=redactIA.select_audio_file)
button_select_audio.pack(pady=5)

label_audio_file = ttk.Label(frame_audio, text="Ningún archivo seleccionado", foreground="blue")
label_audio_file.pack(pady=5)

button_transcribe_audio = ttk.Button(frame_audio, text="Transcribir Audio", command=redactIA.transcribe_audio_handler)
button_transcribe_audio.pack(pady=5)

label_audio_output = ttk.Label(frame_audio, text="Transcripción:")
label_audio_output.pack(pady=5)

text_audio_output = tk.Text(frame_audio, height=10, width=60)
text_audio_output.pack(pady=5)

# Iniciar la aplicación
root.mainloop()
