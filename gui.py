import tkinter as tk
from tkinter import scrolledtext as scrt

from soundmaker import playdiphones
from diphone_converter import converttodiphones


class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Text to speech")
        self.text = scrt.ScrolledText(self.window, width=50, height=15)
        self.text.grid(pady=3, padx=2, columnspan=2)
        insertbutton = tk.Button(text="insert from clipboard", command=self.insertclipboard)
        insertbutton.grid(column=0, sticky="wesn", padx=2, pady=1)
        playbutton = tk.Button(text="play inserted text", command=self.playtext)
        playbutton.grid(column=1, row=1, sticky="wesn", padx=2, pady=1)

    def playtext(self):
        text_content = self.text.get("1.0", "end")
        print("reading text", text_content)
        diphones = converttodiphones(text_content)
        playdiphones(diphones)

    def insertclipboard(self):
        clipboard_content = self.window.clipboard_get()
        self.text.insert("insert", clipboard_content)


ui = Interface()
tk.mainloop()
