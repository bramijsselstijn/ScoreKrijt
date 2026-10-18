#!/usr/bin/env python3
"""Kiosk launcher for the ScoreKrijt box.

Starts the ScoreKrijt application and covers the desktop with a short
fullscreen splash screen while the main application is loading.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk


BASE_DIR = Path(__file__).resolve().parent
APP_SCRIPT = BASE_DIR / "ScoreKrijt.py"
LOGO_PATH = BASE_DIR / "ScoreKrijt" / "icons" / "biljart.png"
SPLASH_SECONDS = 5
BACKGROUND = "#000000"


def start_scorekrijt() -> subprocess.Popen:
    log_path = BASE_DIR / "scorekrijt-autostart.log"
    log_file = log_path.open("a", encoding="utf-8")

    return subprocess.Popen(
        [sys.executable, str(APP_SCRIPT)],
        cwd=str(BASE_DIR),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


def load_logo(root: tk.Tk) -> tk.PhotoImage | None:
    if not LOGO_PATH.exists():
        return None

    try:
        from PIL import Image, ImageTk

        image = Image.open(LOGO_PATH)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        max_width = int(screen_width * 0.45)
        max_height = int(screen_height * 0.45)
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception:
        try:
            return tk.PhotoImage(file=str(LOGO_PATH))
        except tk.TclError:
            return None


def show_splash() -> None:
    root = tk.Tk()
    root.configure(background=BACKGROUND)
    root.overrideredirect(True)
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.config(cursor="none")

    container = tk.Frame(root, background=BACKGROUND)
    container.pack(expand=True, fill="both")

    logo = load_logo(root)
    if logo is not None:
        label = tk.Label(container, image=logo, background=BACKGROUND, borderwidth=0)
        label.image = logo
    else:
        label = tk.Label(
            container,
            text="ScoreKrijt",
            foreground="white",
            background=BACKGROUND,
            font=("DejaVu Serif", 72, "bold"),
        )
    label.place(relx=0.5, rely=0.5, anchor="center")

    def keep_on_top() -> None:
        root.lift()
        root.attributes("-topmost", True)
        root.after(200, keep_on_top)

    keep_on_top()
    root.after(SPLASH_SECONDS * 1000, root.destroy)
    root.mainloop()


def main() -> None:
    start_scorekrijt()
    show_splash()


if __name__ == "__main__":
    main()
