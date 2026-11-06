#!/usr/bin/env python3
"""Kiosk launcher for the ScoreKrijt box.

Starts the ScoreKrijt application and covers the desktop with a fullscreen
splash screen with a loading message until the application reports that it is
ready (by creating the ready file), or until it stops or takes too long.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
import tkinter as tk


BASE_DIR = Path(__file__).resolve().parent
APP_SCRIPT = BASE_DIR / "ScoreKrijt.py"
LOCK_PATH = BASE_DIR / "scorekrijt.lock"
READY_PATH = BASE_DIR / "scorekrijt.ready"
LOGO_PATH = BASE_DIR / "ScoreKrijt" / "icons" / "ScoreKrijt Logo.png"
MIN_SPLASH_SECONDS = 3
MAX_SPLASH_SECONDS = 90
BACKGROUND = "#000000"
LOADING_TEXT = "SK-Box wordt gestart"


def acquire_single_instance_lock():
    """Return an open lock file, or None when ScoreKrijt is already running.

    The lock is inherited by the ScoreKrijt process, so it stays held for as
    long as the application runs and a second launcher exits immediately.
    On systems without fcntl (Windows) no lock is used.
    """
    try:
        import fcntl
    except ImportError:
        return False

    handle = LOCK_PATH.open("w")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        return None
    os.set_inheritable(handle.fileno(), True)
    return handle


def start_scorekrijt(lock_handle=None) -> subprocess.Popen:
    log_path = BASE_DIR / "scorekrijt-autostart.log"
    log_file = log_path.open("a", encoding="utf-8")
    pass_fds = (lock_handle.fileno(),) if lock_handle else ()

    # De applicatie maakt dit bestand aan zodra hij klaar is voor gebruik.
    try:
        READY_PATH.unlink()
    except FileNotFoundError:
        pass
    env = dict(os.environ, SCOREKRIJT_READY_FILE=str(READY_PATH))

    return subprocess.Popen(
        [sys.executable, str(APP_SCRIPT)],
        cwd=str(BASE_DIR),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        pass_fds=pass_fds,
        env=env,
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


def show_splash(process: subprocess.Popen) -> None:
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

    status = tk.Label(
        container,
        text=LOADING_TEXT,
        foreground="#b8b8b8",
        background=BACKGROUND,
        font=("DejaVu Sans", max(14, root.winfo_screenheight() // 40)),
    )
    status.place(relx=0.5, rely=0.84, anchor="center")

    def keep_on_top() -> None:
        root.lift()
        root.attributes("-topmost", True)
        root.after(200, keep_on_top)

    started = time.monotonic()
    step = [0]

    def update_status() -> None:
        elapsed = time.monotonic() - started
        ready = READY_PATH.exists()
        stopped = process.poll() is not None
        if (ready and elapsed >= MIN_SPLASH_SECONDS) or stopped or elapsed >= MAX_SPLASH_SECONDS:
            root.destroy()
            return
        # Bewegende puntjes laten zien dat de SK-Box bezig is en niet is vastgelopen.
        step[0] = (step[0] + 1) % 4
        status.config(text=LOADING_TEXT + "." * step[0] + " " * (3 - step[0]))
        root.after(400, update_status)

    keep_on_top()
    update_status()
    root.mainloop()


def main() -> None:
    lock_handle = acquire_single_instance_lock()
    if lock_handle is None:
        # ScoreKrijt draait al: een tweede start zou Bluetooth en scherm dubbel gebruiken.
        return
    process = start_scorekrijt(lock_handle or None)
    show_splash(process)


if __name__ == "__main__":
    main()
