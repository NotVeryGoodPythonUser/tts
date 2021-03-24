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
        self.play_object = None
        self.window = tk.Tk()
        self.window.minsize(200, 100)
        self.window.title("Syntéza řeči")
        try:
            self.window.iconbitmap("icon.ico")
        except:
            print("Speciální ikona nebude.")
        self.text = scrt.ScrolledText(self.window, width=50, height=15,
                                      wrap=tk.WORD)
        self.text.grid(pady=3, padx=2, sticky="wesn", columnspan=3)
        insertbutton = tk.Button(text="Vložit",
                                 command=self.insert_from_clipboard)
        insertbutton.grid(column=0, sticky="wesn", padx=2, pady=1)
        playbutton = tk.Button(text="Čti!", command=self.play_text)
        playbutton.grid(column=1, row=1, sticky="wesn", padx=2, pady=1)
        self.stopbutton = tk.Button(text="Stop", command=self.stop_playing,
                                    state=tk.DISABLED)
        self.stopbutton.grid(column=2, row=1, sticky="wesn", padx=2, pady=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=2)
        self.window.grid_columnconfigure(1, weight=2)
        self.window.grid_columnconfigure(2, weight=1)

    def stop_playing(self):
        """
        stops playback

        :return: None
        """
        if self.play_object:
            self.play_object.stop()

    def play_text(self):
        """
        plays text from the self.text widget

        :return: None
        """
        def disable_stop_when_done():
            if self.play_object.is_playing():
                self.window.after(500, disable_stop_when_done)
            else:
                self.stopbutton["state"] = tk.DISABLED

        self.stop_playing()
        self.stopbutton["state"] = tk.NORMAL
        print("stopbutton should be normal")
        text_content = self.text.get("1.0", "end")
        print("reading text", text_content)
        diphones = convert_to_diphones(text_content)
        self.play_object = play_diphones(diphones)
        disable_stop_when_done()

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
