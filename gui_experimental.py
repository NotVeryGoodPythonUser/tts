import tkinter as tk
from tkinter import scrolledtext as scrt

from soundmaker import playdiphones
from diphone_converter import converttodiphones

DARK_GRAY = "#2e2c33"
GRAY = "#4c4854"

class Interface:
    def __init__(self):
        self.sidepanel_mode = False
        self.last_geometry = None
        self.last_mouse_pos = {}

        self.window = tk.Tk()
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", 1)
        self.window.geometry("400x300+50+50")
        self.window.bind("<Button-1>", self.get_mouse_pos)


        self.top_panel = tk.Frame(self.window, bg=DARK_GRAY)
        self.top_panel.bind("<B1-Motion>", self.move_window)
        self.quit_button = tk.Button(
            self.top_panel,
            text="✕",
            command=self.window.quit,
            font=("verdena", "10", "bold"),
            width=3,
            fg="orange",
            bg=DARK_GRAY,
            relief="flat",
            overrelief="sunken"
        )
        self.quit_button.pack(side=tk.RIGHT)
        self.side_button = tk.Button(
            self.top_panel,
            text="▯",
            command=self.sidepanel,
            font=("verdena", "10"),
            width=3,
            fg="orange",
            bg=DARK_GRAY,
            relief="flat",
            overrelief="sunken",
        )
        self.side_button.pack(side=tk.RIGHT)
        self.top_panel.pack(fill=tk.X)

        self.top_border = tk.Frame(self.top_panel, cursor="sb_v_double_arrow", bg=DARK_GRAY, height=3)
        self.bottom_border = tk.Frame(self.window, cursor="sb_v_double_arrow", bg=DARK_GRAY, height=3)
        self.left_border = tk.Frame(self.window, cursor="sb_h_double_arrow", bg=DARK_GRAY, width=3)
        self.right_border = tk.Frame(self.window, cursor="sb_h_double_arrow", bg=DARK_GRAY, width=3)
        self.top_border.bind("<B1-Motion>", self.resize)
        self.bottom_border.bind("<B1-Motion>", self.resize)
        self.left_border.bind("<B1-Motion>", self.resize)
        self.right_border.bind("<B1-Motion>", self.resize)

        self.left_border.pack(side=tk.LEFT, fill="y")
        self.top_border.pack(fill="x")
        self.bottom_border.pack(side=tk.BOTTOM, fill="x")
        self.right_border.pack(side=tk.RIGHT, fill="y")

        title = tk.Label(self.top_panel, text="Software text reader", bg=DARK_GRAY, fg="orange")
        title.pack(side="left")
        title.bind("<B1-Motion>", self.move_window)

        tk.Frame(self.window, height=3, bg=DARK_GRAY).pack(fill="x")

        content_frame = tk.Frame(self.window, bg=GRAY, bd=0)
        content_frame.pack(fill="both", expand=True)
        self.text = scrt.ScrolledText(
            content_frame,
            width=170,
            height=150,
            wrap=tk.WORD,
            fg="white",
            bg=GRAY,
            relief="flat"
        )
        self.text.vbar.config(
            bg=GRAY,
            troughcolor="darkgray",
            relief="flat"
        )
        self.text.grid(columnspan=3)
        insertbutton = tk.Button(
            content_frame,
            text="Ctrl+V",
            command=self.insertclipboard,
            bg=GRAY,
            bd=2,
            overrelief="sunken",
            relief="ridge",
        )
        tk.Frame(content_frame, height=2, bd=0, bg=DARK_GRAY).grid(columnspan=3, sticky="we")
        tk.Frame(content_frame, height=3, bd=0, bg=GRAY).grid()

        insertbutton.grid(column=0, sticky="wesn")
        playbutton = tk.Button(
            content_frame,
            text="Read!",
            command=self.playtext,
            bg=GRAY,
            bd=2,
            overrelief="sunken",
            relief="ridge",
        )
        playbutton.grid(column=2, row=3, sticky="wesn")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_columnconfigure(1, minsize=3)

    def sidepanel(self):
        if self.sidepanel_mode == True:
            self.sidepanel_mode = False
            self.side_button.config(text="▯")
            self.window.geometry(self.last_geometry)
        else:
            self.sidepanel_mode = True
            self.side_button.config(text="◻")
            self.last_geometry = self.window.geometry()
            screen_height = self.window.winfo_screenheight()
            screen_width = self.window.winfo_screenwidth()
            self.window.geometry(f"200x{screen_height}+{screen_width-200}+0")

    def get_mouse_pos(self, event):
        self.last_mouse_pos["x"] = event.x
        self.last_mouse_pos["y"] = event.y
        self.last_mouse_pos["abs_x"] = event.x_root
        self.last_mouse_pos["abs_y"] = event.y_root
        self.last_mouse_pos["width"] = self.window.winfo_width()
        self.last_mouse_pos["height"] = self.window.winfo_height()

    def move_window(self, event):
        self.sidepanel_mode = False
        self.side_button.config(text="▯")
        self.window.geometry(
            f"+{event.x_root-self.last_mouse_pos['x']}+{event.y_root - self.last_mouse_pos['y']}"
        )

    def resize(self, event):
        self.sidepanel_mode = False
        self.side_button.config(text="▯")
        width = self.last_mouse_pos["width"]
        height = self.last_mouse_pos["height"]
        x = self.last_mouse_pos["x"]
        y = self.last_mouse_pos["y"]
        abs_x = self.last_mouse_pos["abs_x"]
        abs_y = self.last_mouse_pos["abs_y"]
        if event.widget == self.bottom_border and height + event.y_root - abs_y > 0:
            self.window.geometry(
                f"{width}x{height + event.y_root - abs_y}"
            )
        elif event.widget == self.right_border and width + event.x_root - abs_x:
            self.window.geometry(
                f"{width + event.x_root - abs_x}x{height}"
            )
        elif event.widget == self.top_border and height-event.y_root+abs_y > 0:
            self.window.geometry(
                f"{width}x{height - event.y_root + abs_y}+{abs_x-x}+{event.y_root}"
            )
        elif event.widget == self.left_border and width - event.x_root + abs_x > 0:
            self.window.geometry(
                f"{width - event.x_root + abs_x}x{height}+{event.x_root}+{abs_y-y}"
            )

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
