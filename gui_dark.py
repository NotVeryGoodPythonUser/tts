"""
GUI dark
========
Dark version of graphical user interface for speech synthesis.

Uses tkinter.
Uses custom modules custom_window, custom_scrollbar, soundmaker
and diphone_converter.

Contains class Interface. Creates instance of it when started.
"""

import tkinter as tk

from custom_window import CustomTk
import custom_scrollbar as cs
from soundmaker import play_diphones
from diphone_converter import convert_to_diphones


class Interface:
    """
    dark version of graphical user interface for speech synthesis

    methods
    _______
    * play_text - plays text in the text widget
    * insert_clipboard - inserts text from clipboard into the text widget

    attributes
    __________
    * window - window of the gui, instance of class CustomTk from
        module custom_window
    * text - text widget in which the user inputs text that should
        be read, instance of tkinter.Text
    """
    def __init__(self, *, win_bg="gray15", widg_bg="gray25",
                 widg_fg="orange", text_fg="white"):
        """
        :param str win_bg: color to fill the background of the window with
        :param str widg_bg: color to fill the background of widgets in
            the window
        :param str widg_fg: foreground color of widgets
        :param str text_fg: color of text in the text widget
        """
        self.play_object = None

        self.window = CustomTk(
            title="Syntéza řeči",
            icon="icon_orange.png",
            bg=win_bg,
            fg=widg_fg
        )
        content_frame = self.window.content_frame

        textframe = tk.Frame(content_frame)
        self.text = tk.Text(
            textframe,
            width=200,
            height=150,
            wrap=tk.WORD,
            fg=text_fg,
            bg=widg_bg,
            relief="flat"
        )
        text_scrollbar = cs.Scrollbar(
            textframe,
            command=self.text.yview,
            bg=widg_bg,
            fg=win_bg
        )
        self.text["yscrollcommand"] = text_scrollbar.set
        text_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.text.pack(side=tk.LEFT, expand=1, fill="both")
        textframe.grid(columnspan=3)

        # divider
        tk.Frame(content_frame, height=3, bd=0, bg=win_bg)\
            .grid(columnspan=3, sticky="we")

        insertbutton = tk.Button(
            content_frame,
            text="Vložit",
            command=self.insert_clipboard,
            bg=widg_bg,
            fg=widg_fg,
            bd=2,
            relief="flat",
            overrelief="sunken",
        )
        insertbutton.grid(column=0, sticky="wesn")

        playbutton = tk.Button(
            content_frame,
            text="Čti!",
            command=self.play_text,
            bg=widg_bg,
            fg=widg_fg,
            bd=2,
            relief="flat",
            overrelief="sunken",
        )
        playbutton.grid(column=2, row=2, sticky="wesn")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_columnconfigure(1, minsize=3)

    def play_text(self):
        """
        plays text from the text widget

        :return: None
        """
        if self.play_object:
            self.play_object.stop()
        text_content = self.text.get("1.0", "end")
        print("reading text", text_content)
        diphones = convert_to_diphones(text_content)
        self.play_object = play_diphones(diphones)

    def insert_clipboard(self):
        """
        inserts text from clipboard into the text widget

        inserts the text from clipboard on the position of cursor
        :return: None
        """
        clipboard_content = self.window.clipboard_get()
        self.text.insert("insert", clipboard_content)


if __name__ == "__main__":
    ui = Interface()
    tk.mainloop()
