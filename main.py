from PyQt5.QtWidgets import QApplication

import main_window

app = QApplication([])
window = main_window.MainWindow()
window.show()
app.exec_()