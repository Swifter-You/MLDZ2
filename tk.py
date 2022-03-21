import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from vosk import Model, KaldiRecognizer
import sys
import json
import os
import time
import wave
import re

def open_file():
    filepath = askopenfilename(
        filetypes=[("Аудио файлы", "*.wav"), ("Все файлы", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "rb") as input_file:
        result = trans(input_file)
        txt_edit.insert(tk.END, result)
    window.title(f"Транскрибуция - {filepath}")

def trans(fileObj):
    model = Model('./vosk-model-small-ru-0.22')
    inputfile = fileObj
    wf = wave.open(inputfile, "r")
    rcgn_fr = wf.getframerate() * wf.getnchannels()
    rec = KaldiRecognizer(model, rcgn_fr)
    result = ''
    last_n = False
    #read_block_size = 4000 
    read_block_size = wf.getnframes()
    while True:
        data = wf.readframes(read_block_size)
        if len(data) == 0:
            break
    
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            
            if res['text'] != '':
                result += f" {res['text']}"
                if read_block_size < 200000:
                    print(res['text'] + " \n")
                
                last_n = False
            elif not last_n:
                result += '\n'
                last_n = True
    
    res = json.loads(rec.FinalResult())
    result += f" {res['text']}"    
    return result


def save_file():
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Транскрибуция - {filepath}")
 
 
window = tk.Tk()
window.title("Транскрибуция")
window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=500, weight=1)
 
txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Открыть", command=open_file)
btn_save = tk.Button(fr_buttons, text="Сохранить как...", command=save_file)
 
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
 
fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")
 
window.mainloop()