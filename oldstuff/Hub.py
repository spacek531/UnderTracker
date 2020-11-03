import os
from pathlib import Path

from PyQt5 import QtCore, QtWidgets, QtGui

import main_windows


class Hub(QtCore.QObject):
    window_quit_signal = QtCore.pyqtSignal(bool)  # if window was closed, close ahk script
    quit_worker_signal = QtCore.pyqtSignal()

    def __init__(self, crash_handler):
        super().__init__()

        crash_handler.traceback_sig.connect(self.show_exception)
        self.application = QtWidgets.QApplication.instance()

        self.main_window = main_windows.MainWindow(self)
        self.crash_window = popups.CrashPop()

    def startup(self):
        self.write_default_settings()
        self.set_theme()
        self.double_signal = self.main_window.double_signal
        self.edit_signal = self.main_window.edit_signal
        self.show_window()
        self.initial_pop()

    def show_window(self):
        # check for old settings
        if (self.settings.value("window/geometry") is None
                and self.settings.value("window/pos", type=QtCore.QPoint)
                and self.settings.value("window/size", type=QtCore.QSize)):
            self.main_window.resize(self.settings.value("window/size", type=QtCore.QSize))
            self.main_window.move(self.settings.value("window/pos", type=QtCore.QPoint))
        else:
            self.main_window.restoreGeometry(self.settings.value("window/geometry"))
        font = self.settings.value("font/font", type=QtGui.QFont)
        font.setPointSize(self.settings.value("font/size", type=int))
        font.setBold(self.settings.value("font/bold", type=bool))
        autoscroll = self.settings.value("window/autoscroll", type=bool)
        self.main_window.change_settings(font, self.dark, autoscroll)
        self.main_window.show()

    def set_theme(self):
        """Set dark/default theme depending on user setting"""
        if self.dark:
            change_to_dark()
        else:
            change_to_default()

    def initial_pop(self):
        w = main_windows.PlotStartDialog(self.main_window, self.settings)
        w.setup_ui()
        w.show()
        w.after_show()

    def end_route_pop(self):
        w = popups.RouteFinishedPop(self.main_window)
        w.show()
        w.close_signal.connect(self.main_window.disconnect_signals)
        w.new_route_signal.connect(self.new_route)

    def licenses_pop(self):
        w = popups.LicensePop(self.main_window)
        w.show()
        w.close_signal.connect(lambda:
                               self.main_window.about_action.setEnabled(True))
        self.main_window.about_action.setDisabled(True)

    def sett_pop(self):
        w = popups.SettingsPop(self.main_window, self.settings)
        w.show()
        w.settings_signal.connect(self.change_editable_settings)
        w.close_signal.connect(lambda:
                               self.main_window.settings_action.setEnabled(True))
        self.main_window.settings_action.setDisabled(True)

    def show_exception(self, exc):
        self.crash_window.add_traceback(exc)
        self.crash_window.show()

    def quit(self, geometry):
        #self.settings.setValue("window/geometry", geometry)
        #self.settings.sync()
        self.window_quit_signal.emit(self.save_on_quit)


def change_to_dark():
    p = QtGui.QPalette()
    p.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    p.setColor(QtGui.QPalette.WindowText, QtGui.QColor(247, 247, 247))
    p.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    p.setColor(QtGui.QPalette.Text, QtGui.QColor(247, 247, 247))
    p.setColor(QtGui.QPalette.Button, QtGui.QColor(60, 60, 60))
    p.setColor(QtGui.QPalette.Background, QtGui.QColor(35, 35, 35))
    p.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(45, 45, 45))
    p.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    p.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    p.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(0, 0, 0))
    p.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(110, 110, 100))
    app = QtWidgets.QApplication.instance()
    app.setStyle("Fusion")
    app.setPalette(p)


def change_to_default():
    app = QtWidgets.QApplication.instance()
    app.setStyle("Fusion")
    app.setPalette(app.style().standardPalette())