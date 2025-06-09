import sys
from PyQt6.QtWidgets import QApplication

from pap import kecewa

app = QApplication(sys.argv)
window = kecewa()
window.show()
app.exec()