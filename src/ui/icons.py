import os

from PyQt6.QtGui import QIcon


ICON_DIRECTORY = os.path.join("../icons")
ICON_FILE_EXTENSION = ".png"


def get_custom_icon(icon_name: str):
    file_path = os.path.join(ICON_DIRECTORY, icon_name + ".png")
    assert os.path.isfile(file_path)
    return QIcon(file_path)
