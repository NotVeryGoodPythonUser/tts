import tkinter as tk

from custom_window import custom_Tk
import special_scrollbar as ss
from soundmaker import playdiphones
from diphone_converter import converttodiphones

DARK_GRAY = "#2e2c33"
GRAY = "#4c4854"


class Interface:
    def __init__(self):
        self.play_object = None

        content_frame = custom_Tk(title="Text reader" ,icon="🗨👄").content_frame
        textframe = tk.Frame(content_frame)
        self.text = tk.Text(
            textframe,
            width=200,
            height=150,
            wrap=tk.WORD,
            fg="white",
            bg=GRAY,
            relief="flat"
        )
        self.text_scrollbar = ss.Scrollbar(
            textframe,
            command=self.text.yview,
            bg=GRAY,
            fg=DARK_GRAY
        )
        self.text["yscrollcommand"] = self.text_scrollbar.set
        self.text_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.text.pack(side=tk.LEFT, expand=1, fill="both")
        textframe.grid(columnspan=3)

        tk.Frame(content_frame, height=3, bd=0, bg=DARK_GRAY).grid(columnspan=3, sticky="we")

        insertbutton = tk.Button(
            content_frame,
            text="Ctrl+V",
            command=self.insertclipboard,
            bg=GRAY,
            bd=2,
            relief="flat",
            overrelief="sunken",
        )

        insertbutton.grid(column=0, sticky="wesn")
        playbutton = tk.Button(
            content_frame,
            text="Read!",
            command=self.playtext,
            bg=GRAY,
            bd=2,
            relief="flat",
            overrelief="sunken",
        )
        playbutton.grid(column=2, row=2, sticky="wesn")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_columnconfigure(1, minsize=3)


    def playtext(self):
        if self.play_object:
            self.play_object.stop()
        text_content = self.text.get("1.0", "end")
        print("reading text", text_content)
        diphones = converttodiphones(text_content)
        self.play_object = playdiphones(diphones)

    def insertclipboard(self):
        clipboard_content = self.window.clipboard_get()
        self.text.insert("insert", clipboard_content)


ui = Interface()
tk.mainloop()
