"""
Custom window
=============
Contains class CustomTk which extends class tkinter.Tk.
  + window is always on top, style of it's title bar can be changed
  - isn't visible on taskbar, can not be iconified
"""
import tkinter as tk
import os


class CustomTk(tk.Tk):
    """
    Class extending class tkinter.Tk to allow style changes.

    + window is always on top, style of it's title bar can be changed
    - isn't visible on taskbar, can not be iconified

    methods
    _______
    * pack_all - packs all widgets into the window.
    * unpack_all - forgets pack of most widgets to allow minimising
    * sidepanel - switches sidepanel mode and of
    * make_small - minimises the window to show only icon and two buttons
    * get_mouse_pos - tracks position of cursor to allow resizing and moving of
        the window, called only by mouse event
    * move_window - moves the window, called only by mouse event
    * resize - resizes window, has to be called by mouse event

    attributes
    __________
    * content_frame - main frame of the window, where all content should be
        inserted, Instance of tkinter.Frame
    * title - widget representing title of the window, instance of
        tkinter.Label
    * icon - widget representing icon of the window, instance of
        tkinter.Label
    """
    def __init__(self, *, title="dark window",
                 icon="シ", bg="gray15", fg="orange"):
        """
        :param str title: short string that should be showed in the title bar,
                default is "dark window"
        :param str icon: either path to image that should be used as an icon in
                title bar or short string that should be used as an icon,
                default is "シ"
        :param str bg: color that should be used as a background of the
                window, default is "gray15"
        :param str fg: color that should be used as a foreground of the window,
                default is "orange"
        """

        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)
        self.geometry("400x300+50+50")
        self.bind("<Button-1>", self.get_mouse_pos)
        self.config(bg=bg)

        self.sidepanel_mode = False
        self.last_geometry = None
        self.small_mode = False
        self.last_mouse_pos = {}
        self.max_size = [150, 180]

    # ================ title bar =====================
        self.title_bar = tk.Frame(self, bg=bg)
        self.title_bar.bind("<B1-Motion>", self.move_window)

        # titlebar buttons
        self.quit_button = tk.Button(
            self.title_bar,
            text="✕",
            command=self.quit,
            font=("verdena", "10", "bold"),
            width=3,
            fg=fg,
            bg=bg,
            relief="flat",
            overrelief="sunken"
        )
        self.side_button = tk.Button(
            self.title_bar,
            text="▯",
            command=self.sidepanel,
            font=("verdena", "10"),
            width=3,
            fg=fg,
            bg=bg,
            relief="flat",
            overrelief="sunken",
        )
        self.small_button = tk.Button(
            self.title_bar,
            text="_",
            command=self.make_small,
            font=("verdena", "10"),
            width=3,
            fg=fg,
            bg=bg,
            relief="flat",
            overrelief="sunken",
        )

        # icon and title
        if os.path.exists(icon):
            self.icon_image = tk.PhotoImage(file=icon)
            if self.icon_image.height() > 30:
                self.icon_image.subsample(self.icon_image.height()//30)
            self.icon = tk.Label(
                self.title_bar,
                image=self.icon_image,
                font="courier 15",
                bg=bg,
                fg=fg
            )
        else:
            self.icon = tk.Label(
                self.title_bar,
                text=icon,
                font="courier 15",
                bg=bg,
                fg=fg
            )
        self.icon.bind("<B1-Motion>", self.move_window)


        self.title = tk.Label(
            self.title_bar,
            text=title,
            font="arial 10",
            bg=bg,
            fg=fg
        )
        self.title.bind("<B1-Motion>", self.move_window)

    # ========================== borders ===============================
        self.top_border = tk.Frame(
            self.title_bar,
            cursor="sb_v_double_arrow",
            bg=bg,
            height=3
        )
        self.bottom_border = tk.Frame(
            self,
            cursor="sb_v_double_arrow",
            bg=bg,
            height=3
        )
        self.left_border = tk.Frame(
            self,
            cursor="sb_h_double_arrow",
            bg=bg,
            width=3
        )
        self.right_border = tk.Frame(
            self,
            cursor="sb_h_double_arrow",
            bg=bg,
            width=3
        )
        self.top_border.bind("<B1-Motion>", self.resize)
        self.bottom_border.bind("<B1-Motion>", self.resize)
        self.left_border.bind("<B1-Motion>", self.resize)
        self.right_border.bind("<B1-Motion>", self.resize)

        self.left_border.pack(side=tk.LEFT, fill="y")
        self.top_border.pack(fill="x")
        self.bottom_border.pack(side=tk.BOTTOM, fill="x")
        self.right_border.pack(side=tk.RIGHT, fill="y")

        tk.Frame(self, height=3, bg=bg).pack(fill="x")

        self.content_frame = tk.Frame(self, bg=bg, bd=0)
        self.pack_all()

    def pack_all(self):
        """
        Packs all window widgets into the window.

        :return: None
        """
        self.quit_button.pack(side=tk.RIGHT)
        self.side_button.pack(side=tk.RIGHT)
        self.small_button.pack(side=tk.RIGHT)
        self.icon.pack(side="left")
        self.title.pack(side="left")
        self.title_bar.pack(fill=tk.X)

        self.left_border.pack(side=tk.LEFT, fill="y")
        self.top_border.pack(fill="x")
        self.bottom_border.pack(side=tk.BOTTOM, fill="x")
        self.right_border.pack(side=tk.RIGHT, fill="y")

        self.content_frame.pack(fill="both", expand=True)

    def unpack_all(self):
        """
        Forgets packing of most widgets to allow minimising of the window.

        :return: None
        """
        self.quit_button.pack_forget()
        self.side_button.pack_forget()
        self.small_button.pack_forget()
        self.icon.pack_forget()
        self.title.pack_forget()
        self.title_bar.pack_forget()

        self.left_border.pack_forget()
        self.top_border.pack_forget()
        self.bottom_border.pack_forget()
        self.right_border.pack_forget()

        self.content_frame.pack_forget()
        print("all packs forgotten")

    def sidepanel(self):
        """
        Switches sidepanel mode on and off.

        :return: None
        """
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
        """
        Minimises the window to contain only icon and two buttons or
        makes the window normal again if minimised

        :return: None
        """
        if self.small_mode:
            self.quit_button.pack_forget()
            self.small_button.pack_forget()
            self.icon.pack_forget()
            self.title_bar.pack_forget()
            last_size = self.last_geometry[:self.last_geometry.index("+")]
            self.geometry(last_size)
            self.pack_all()
            self.small_button.config(text="_")
            self.small_mode = False
        else:
            self.unpack_all()
            self.quit_button.pack(side=tk.RIGHT)
            self.small_button.pack(side=tk.RIGHT)
            self.icon.pack(side="left")
            self.title_bar.pack(fill=tk.X)
            if not self.sidepanel_mode:
                self.last_geometry = self.geometry()
            width = 10
            width += self.icon.winfo_width()
            width += self.small_button.winfo_width()
            width += self.quit_button.winfo_width()
            self.geometry(f"{width}x30")
            self.small_button.config(text="◻")
            self.small_mode = True

    def get_mouse_pos(self, event):
        """
        Tracks position of cursor to allow resizing and moving of the
        window. Has to be called by mouse event.

        :return: None
        """
        self.last_mouse_pos["x"] = event.x
        self.last_mouse_pos["y"] = event.y
        self.last_mouse_pos["abs_x"] = event.x_root
        self.last_mouse_pos["abs_y"] = event.y_root
        self.last_mouse_pos["width"] = self.winfo_width()
        self.last_mouse_pos["height"] = self.winfo_height()

    def move_window(self, event):
        """
        Moves the window. has to be called by button motion event.
        Bound to title bar of the window.

        :return: None
        """
        self.sidepanel_mode = False
        self.side_button.config(text="▯")
        self.geometry(f"+{event.x_root-self.last_mouse_pos['x']}"
                      f"+{event.y_root - self.last_mouse_pos['y']}")

    def resize(self, event):
        """
        Resizes window. has to be called by button motion event.
        Bound to borders of the window.

        :return: None
        """
        self.sidepanel_mode = False
        self.side_button.config(text="▯")
        width = self.last_mouse_pos["width"]
        height = self.last_mouse_pos["height"]
        x = self.last_mouse_pos["x"]
        y = self.last_mouse_pos["y"]
        abs_x = self.last_mouse_pos["abs_x"]
        abs_y = self.last_mouse_pos["abs_y"]
        if event.widget == self.bottom_border:
            if height + event.y_root - abs_y > self.max_size[1]:
                self.geometry(
                    f"{width}x{height + event.y_root - abs_y}"
                )
            else:
                self.geometry(
                    f"{width}x{self.max_size[1]}"
                )
        elif event.widget == self.right_border:
            if width + event.x_root - abs_x > self.max_size[0]:
                self.geometry(
                    f"{width + event.x_root - abs_x}x{height}"
                )
            else:
                self.geometry(
                    f"{self.max_size[0]}x{height}"
                )
        elif event.widget == self.top_border:
            if height-event.y_root+abs_y > self.max_size[1]:
                self.geometry(
                    f"{width}x{height - event.y_root + abs_y}"
                    f"+{abs_x-x}+{event.y_root}"
                )
            else:
                self.geometry(
                    f"{width}x{self.max_size[1]}"
                    f"+{abs_x - x}+{abs_y+height-self.max_size[1]}"
                )
        elif event.widget == self.left_border:
            if width - event.x_root + abs_x > self.max_size[0]:
                self.geometry(
                    f"{width - event.x_root + abs_x}x{height}"
                    f"+{event.x_root}+{abs_y-y}"
                )
            else:
                self.geometry(
                    f"{self.max_size[0]}x{height}"
                    f"+{abs_x+width-self.max_size[0]}+{abs_y - y}"
                )
