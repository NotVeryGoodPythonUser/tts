"""
custom scrollbar
================
This module provides custom version of scrollbar, which unlike usual
tkinter scrollbar can have different colors.

Supports only vertical orientation.

Contains one class Scrollbar, which extends class tkinter.Frame.
"""
import tkinter as tk


class Scrollbar(tk.Frame):
    """
    custom version of scrollbar

    supports only vertical orientation, its colors can by changed

    to connect scrollbar with another widgets use the widget's method
    yview as Scrollbar's parameter command and scrollbar's method .set
    as the widget's parameter yscrollcommand

    Methods
    -------
    * set - sets position of the slider in the trough, designed to be
        set as yscrollcomand of another widget
    * up_button_handler - scrolls connected widget up
    * down_button_handler - scrolls connected widget down
    * drag_slider - scrolls connected widget when dragging the slider
    * correct_slider_width - called after initiation to adjust width of
        the slider to fit into the trough
    """
    def __init__(self, master, *, bg="lightgray", fg="darkgray",
                 width=16, length=100,
                 command=lambda top, bottom: print("command not specified")):
        """
        :param tk.Frame master: widget to pack or grid the scrollbar in
        :param str bg: color to fill the trough and background
            of the buttons with
        :param str fg: color to fill slider and foreground of buttons with
        :param int width: width of the scrollbar
        :param int length: length of the scrollbar
        :param callable command: yview method of widget that should be
            connected to the scrollbar
        """
        self.command = command
        self.last_set = 0, 1
        super().__init__(master, bg=bg, width=width, height=length)
        self.trough = tk.Frame(self, width=width, height=length - 30)
        self.button_up = tk.Button(
            self,
            text="▲",
            font=("impact", str(width // 2), "bold"),
            justify="center",
            width=1,
            command=self.up_button_handler,
            repeatdelay=500,
            repeatinterval=50,
            relief="flat",
            bg=bg,
            fg=fg,
            activebackground=fg,
            activeforeground=bg,
            bd=0
        )
        self.button_down = tk.Button(
            self,
            text="▼",
            font=("impact", str(width // 2), "bold"),
            width=1,
            command=self.down_button_handler,
            repeatdelay=500,
            repeatinterval=50,
            relief="flat",
            bg=bg,
            fg=fg,
            activebackground=fg,
            activeforeground=bg,
            bd=0

        )

        self.trough["relief"] = "flat"
        self.trough["bg"] = bg
        self.button_up.pack(side=tk.TOP, fill="both")
        self.trough.pack(side=tk.TOP, fill="both", expand=1)
        self.button_down.pack(side=tk.TOP, fill="both")
        self.slider = tk.Canvas(
            self.trough,
            width=1,
            height=length,
            highlightbackground=bg,
            bg=fg,
        )
        self.slider.place(x=0, y=0)
        self.slider.bind("<B1-Motion>", self.drag_slider)
        self.after(10, self.correct_slider_width)
        self.mouse_pos = None

    def correct_slider_width(self):
        """
        corrects width of the slider

        :return: None
        """
        self.update()
        slider_width = self.trough.winfo_width() - 5
        self.slider["width"] = slider_width
        self.slider.place(x=1)

    def set(self, top, bottom):
        """
        sets the slider to the given position

        to connect another widget to the scrollbar use the set method
        as yscrollcommand of that widget

        :param float top: position of the top of the slider, float
            between 0 and 1 (0 is top, 1 is bottom)
        :param float bottom: position of the bottom of the slider, float
            between 0 and 1 (0 is top, 1is bottom)
        :return: None
        """
        top, bottom = float(top), float(bottom)
        self.update()
        trough_height = self.trough.winfo_height()
        slider_height = int(trough_height * (bottom - top))
        self.slider.place(rely=top)
        self.slider["height"] = slider_height
        self.last_set = top, bottom

    def up_button_handler(self):
        """
        moves connected widget up

        :return: None
        """
        top, bottom = self.last_set
        offset = (bottom - top) / 20
        if top - offset > 0:
            self.command(tk.MOVETO, top - offset)
        else:
            self.command(tk.MOVETO, 0)

    def down_button_handler(self):
        """
        moves connected widget down

        :return: None
        """
        top, bottom = self.last_set
        offset = (bottom - top) / 20
        if bottom + offset < 1:
            self.command(tk.MOVETO, top + offset)

        else:
            self.command(tk.MOVETO, 1 + bottom - top)

    def drag_slider(self, event):
        """
        handles dragging of slider using mouse

        :return: None
        """
        in_trough = (self.trough.winfo_pointery() - self.trough.winfo_rooty())
        half_of_slider = ((self.last_set[1] - self.last_set[0]) * self.trough.winfo_height()) // 2
        if in_trough < half_of_slider:
            in_trough = half_of_slider
        elif in_trough > self.trough.winfo_height() - half_of_slider:
            in_trough = self.trough.winfo_height() - half_of_slider
        self.command(
            tk.MOVETO,
            (in_trough - half_of_slider) / self.trough.winfo_height(),
        )
