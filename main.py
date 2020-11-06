from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import main_window

app = QApplication([])
window = main_window.MainWindow()
window.show()
app.setWindowIcon(QIcon(":/resources/tracker.ico"))
window.setWindowIcon(QIcon(":/resources/tracker.ico"))
app.exec_()