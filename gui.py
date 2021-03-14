"""
GUI
===
Basic version of graphical user interface for speech synthesis

uses tkinter.
uses custom modules soundmaker and diphone_converter.


Contains one class Interface. Creates instance of it when started.
"""
import tkinter as tk
from tkinter import scrolledtext as scrt

from soundmaker import play_diphones
from preparation.diphone_converter import convert_to_diphones


class Interface:
    """
    basic version of graphical user interface for speech synthesis

    methods
    _______
    * play_text - plays text in the text widget
    * insert_from_clipboard - inserts text from clipboard into the text widget

    attributes
    __________
    * window - window of the gui, instance of tkinter.Tk
    * text - text widget in which the user inputs text that should
        be read, instance of tkinter.scrolledtext.ScrolledText
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.minsize(200, 100)
        self.window.title("Text to speech")
        self.window.iconbitmap("icon.ico")
        self.text = scrt.ScrolledText(self.window, width=50, height=15)
        self.text.grid(pady=3, padx=2, sticky="wesn", columnspan=2)
        insertbutton = tk.Button(text="insert from clipboard", command=self.insert_from_clipboard)
        insertbutton.grid(column=0, sticky="wesn", padx=2, pady=1)
        playbutton = tk.Button(text="play inserted text", command=self.playtext)
        playbutton.grid(column=1, row=1, sticky="wesn", padx=2, pady=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

    def playtext(self):
        """
        plays text from the self.text widget
        :return: None
        """
        text_content = self.text.get("1.0", "end")
        print("reading text", text_content)
        diphones = convert_to_diphones(text_content)
        play_diphones(diphones)

    def insert_from_clipboard(self):
        """
        inserts text from clipboard into self.text widget
        :return: None
        """
        clipboard_content = self.window.clipboard_get()
        self.text.insert("insert", clipboard_content)

if __name__ == '__main__':
    ui = Interface()
    tk.mainloop()
