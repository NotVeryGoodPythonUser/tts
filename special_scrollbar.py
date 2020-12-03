import tkinter as tk


class Scrollbar(tk.Frame):
    def __init__(self, master, *, bg="lightgray", fg="darkgray", width=16, length=100,
                 command=lambda top, bottom: print("command not specified")):
        self.command = command
        self.button_chars = ("▲", "▼")
        super().__init__(master, bg=bg, width=width, height=length)
        self.trough = tk.Frame(self, width=width, height=length - 30)
        self.button_up = tk.Button(
            self,
            text=self.button_chars[0],
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
            text=self.button_chars[1],
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
        self.update()
        slider_width = self.trough.winfo_width() - 5
        self.slider["width"] = slider_width
        self.slider.place(x=1)

    def set(self, top, bottom):
        top, bottom = float(top), float(bottom)
        self.update()
        trough_height = self.trough.winfo_height()
        slider_height = int(trough_height * (bottom - top))
        self.slider.place(rely=top)
        self.slider["height"] = slider_height
        self.last_set = top, bottom

    def up_button_handler(self):
        top, bottom = self.last_set
        offset = (bottom - top) / 20
        if top - offset > 0:
            self.command(tk.MOVETO, top - offset)
        else:
            self.command(tk.MOVETO, 0)

    def down_button_handler(self):
        top, bottom = self.last_set
        offset = (bottom - top) / 20
        if bottom + offset < 1:
            self.command(tk.MOVETO, top + offset)

        else:
            self.command(tk.MOVETO, 1 + bottom - top)

    def drag_slider(self, event):
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
