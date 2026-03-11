import os
import sys
from PySide6.QtGui import QIcon


def get_icon_path() -> str:
    """Resolve caminho do icone para dev e executavel (PyInstaller)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    ico_path = os.path.join(base_dir, "images", "GAIA_icon.ico")
    if os.path.exists(ico_path):
        return ico_path

    return os.path.join(base_dir, "images", "GAIA_icon.png")


def get_window_icon() -> QIcon:
    return QIcon(get_icon_path())
