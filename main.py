import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from vosk import Model, KaldiRecognizer, SpkModel
import json
import os
import wave


def start():
    def return_to_mainWindow():
        mainWindow.deiconify()
        window_text.destroy()

    def converter_to_text(wavfile):
        model_path = "vosk-model-ru-0.22"
        spk_model_path = "vosk-model-spk-0.4"

        if not os.path.exists(model_path):
            print( "Please download the model from https://alphacephei.com/vosk/models and unpack as {} in the current folder.".format(model_path))
            exit(1)

        if not os.path.exists(spk_model_path):
            print( "Please download the speaker model from https://alphacephei.com/vosk/models and unpack as {} in the current folder.".format(spk_model_path))
            exit(1)

        model = Model(model_path)
        spk_model = SpkModel(spk_model_path)

        wf = wave.open(wavfile, "rb")
        if wf.getsampwidth() != 2:
            print("Audio file must be WAV format PCM. sampwidth=", wf.getsampwidth())
            exit(1)

        if wf.getcomptype() != "NONE":
            print("Audio file must be WAV format PCM. comptype=", wf.getcomptype())
            exit(1)

        rec = KaldiRecognizer(model, wf.getframerate() * wf.getnchannels(), spk_model)
        rec.SetSpkModel(spk_model)

        wf.rewind()
        result = ""
        for i in range(1080):
            data = wf.readframes(4000)
            datalen = len(data)
            if datalen == 0:
                res = json.loads(rec.FinalResult())
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                result = result+'Speaker:'+res['text'] + '\n'
            if datalen == 0:
                break
        return result

    window_text = tk.Toplevel(mainWindow)
    mainWindow.withdraw()
    window_text.title("Речь")
    window_text.geometry("650x200")

    frame_text = tk.Frame(window_text)
    frame_text.pack()
    txt = converter_to_text(link_file.get())
    frame_text.configure(bg='snow')
    t = tk.Text(frame_text, height=20, width=100)
    scroll = tk.Scrollbar(frame_text, command=t.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    t.config(yscrollcommand=scroll.set)
    t.insert('insert', txt)
    t.pack()

    btn = ttk.Button(frame_text, text='Назад', command=lambda: return_to_mainWindow())
    btn.place(x=550, y=0)


def select_file():
    filetypes = [('audio files', '.wav'), ('all files', '.*')]
    filename = fd.askopenfilename(title='Выбрать файл', initialdir='/', filetypes=filetypes)
    link_file.insert(0, filename)


mainWindow = tk.Tk()
mainWindow.title('Распознавание текста')
mainWindow.geometry('450x150')

frame_main = tk.Frame(mainWindow)
frame_main.pack(expand=True, fill=tk.BOTH)
bg = tk.PhotoImage(file="pic.png")
label1 = tk.Label(frame_main, image=bg)
label1.place(x=0, y=0)

link_file = tk.Entry(frame_main)
link_file.place(x=50, y=57)

open_button = ttk.Button(frame_main, text='Открыть файл', command=lambda: select_file())
open_button.place(x=200, y=55)

main_button = ttk.Button(frame_main, text='Получение текста', command=lambda: start())
main_button.place(x=300, y=55)

close_button = tk.Button(frame_main, text="Выйти", command=mainWindow.destroy)
close_button.place(x=350, y=0)

mainWindow.mainloop()
