import tkinter as tk
import os

DARK_GRAY = "#2e2c33"
GRAY = "#4c4854"


class custom_Tk(tk.Tk):
    def __init__(self, *, title="special dark window", icon="シ"):
        if os.path.exists(icon):
            icon_image = icon
        else:
            icon_image = None
            icon_text = icon
        del(icon)
        title_text = title
        del(title)
        self.sidepanel_mode = False
        self.last_geometry = None
        self.small_mode = False
        self.last_mouse_pos = {}

        super().__init__()

        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)
        self.geometry("400x300+50+50")
        self.bind("<Button-1>", self.get_mouse_pos)

        self.top_panel = tk.Frame(self, bg=DARK_GRAY)
        self.top_panel.bind("<B1-Motion>", self.move_window)
        self.quit_button = tk.Button(
            self.top_panel,
            text="✕",
            command=self.quit,
            font=("verdena", "10", "bold"),
            width=3,
            fg="orange",
            bg=DARK_GRAY,
            relief="flat",
            overrelief="sunken"
        )
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
        self.small_button = tk.Button(
            self.top_panel,
            text="_",
            command=self.make_small,
            font=("verdena", "10"),
            width=3,
            fg="orange",
            bg=DARK_GRAY,
            relief="flat",
            overrelief="sunken",
        )

        self.top_border = tk.Frame(self.top_panel, cursor="sb_v_double_arrow", bg=DARK_GRAY, height=3)
        self.bottom_border = tk.Frame(self, cursor="sb_v_double_arrow", bg=DARK_GRAY, height=3)
        self.left_border = tk.Frame(self, cursor="sb_h_double_arrow", bg=DARK_GRAY, width=3)
        self.right_border = tk.Frame(self, cursor="sb_h_double_arrow", bg=DARK_GRAY, width=3)
        self.top_border.bind("<B1-Motion>", self.resize)
        self.bottom_border.bind("<B1-Motion>", self.resize)
        self.left_border.bind("<B1-Motion>", self.resize)
        self.right_border.bind("<B1-Motion>", self.resize)

        self.left_border.pack(side=tk.LEFT, fill="y")
        self.top_border.pack(fill="x")
        self.bottom_border.pack(side=tk.BOTTOM, fill="x")
        self.right_border.pack(side=tk.RIGHT, fill="y")

        if icon_image:
            self.icon_image = tk.PhotoImage(file=icon_image)
            if self.icon_image.height()>30:
                self.icon_image.subsample(self.icon_image.height()//30)
            self.icon = tk.Label(self.top_panel, image=self.icon_image, font="courier 15", bg=DARK_GRAY, fg="orange")
        else:
            self.icon = tk.Label(self.top_panel, text=icon_text, font="courier 15", bg=DARK_GRAY, fg="orange")
        self.icon.bind("<B1-Motion>", self.move_window)
        self.title = tk.Label(self.top_panel, text=title_text, font="arial 10", bg=DARK_GRAY, fg="orange")
        self.title.bind("<B1-Motion>", self.move_window)

        tk.Frame(self, height=3, bg=DARK_GRAY).pack(fill="x")

        self.content_frame = tk.Frame(self, bg=DARK_GRAY, bd=0)
        self.pack_all()

    def pack_all(self):
        self.quit_button.pack(side=tk.RIGHT)
        self.side_button.pack(side=tk.RIGHT)
        self.small_button.pack(side=tk.RIGHT)
        self.icon.pack(side="left")
        self.title.pack(side="left")
        self.top_panel.pack(fill=tk.X)

        self.left_border.pack(side=tk.LEFT, fill="y")
        self.top_border.pack(fill="x")
        self.bottom_border.pack(side=tk.BOTTOM, fill="x")
        self.right_border.pack(side=tk.RIGHT, fill="y")

        self.content_frame.pack(fill="both", expand=True)

    def unpack_all(self):
        self.quit_button.pack_forget()
        self.side_button.pack_forget()
        self.small_button.pack_forget()
        self.icon.pack_forget()
        self.title.pack_forget()
        self.top_panel.pack_forget()

        self.left_border.pack_forget()
        self.top_border.pack_forget()
        self.bottom_border.pack_forget()
        self.right_border.pack_forget()

        self.content_frame.pack_forget()
        print("all packs forgotten")

    def sidepanel(self):
        if self.sidepanel_mode:
            self.sidepanel_mode = False
            self.side_button.config(text="▯")
            self.geometry(self.last_geometry)
        else:
            self.sidepanel_mode = True
            self.side_button.config(text="◻")
            self.last_geometry = self.geometry()
            screen_height = self.winfo_screenheight()
            screen_width = self.winfo_screenwidth()
            self.geometry(f"200x{screen_height}+{screen_width-200}+0")

    def make_small(self):
        if self.small_mode:
            self.quit_button.pack_forget()
            self.small_button.pack_forget()
            self.icon.pack_forget()
            self.top_panel.pack_forget()
            last_size = self.last_geometry[:self.last_geometry.index("+")]
            self.geometry(last_size)
            self.pack_all()
            self.small_button.config(text="_")
            self.small_mode=False
        else:
            self.unpack_all()
            self.quit_button.pack(side=tk.RIGHT)
            self.small_button.pack(side=tk.RIGHT)
            self.icon.pack(side="left")
            self.top_panel.pack(fill=tk.X)
            self.last_geometry = self.geometry()
            width = 10
            width += self.icon.winfo_width()
            width += self.small_button.winfo_width()
            width += self.quit_button.winfo_width()
            self.geometry(f"{width}x30")
            self.small_button.config(text="◻")
            self.small_mode = True

    def get_mouse_pos(self, event):
        self.last_mouse_pos["x"] = event.x
        self.last_mouse_pos["y"] = event.y
        self.last_mouse_pos["abs_x"] = event.x_root
        self.last_mouse_pos["abs_y"] = event.y_root
        self.last_mouse_pos["width"] = self.winfo_width()
        self.last_mouse_pos["height"] = self.winfo_height()

    def move_window(self, event):
        self.sidepanel_mode = False
        self.side_button.config(text="▯")
        self.geometry(
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
            self.geometry(
                f"{width}x{height + event.y_root - abs_y}"
            )
        elif event.widget == self.right_border and width + event.x_root - abs_x:
            self.geometry(
                f"{width + event.x_root - abs_x}x{height}"
            )
        elif event.widget == self.top_border and height-event.y_root+abs_y > 0:
            self.geometry(
                f"{width}x{height - event.y_root + abs_y}+{abs_x-x}+{event.y_root}"
            )
        elif event.widget == self.left_border and width - event.x_root + abs_x > 0:
            self.geometry(
                f"{width - event.x_root + abs_x}x{height}+{event.x_root}+{abs_y-y}"
            )
