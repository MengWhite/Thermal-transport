import os
os.environ['OVITO_GUI_MODE'] = '1'

from GUI.main_window_2 import MainWindow
from output import render_3d

from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()

render_3d.insert_widget(window.painting_zoom)

sys.exit(app.exec())
