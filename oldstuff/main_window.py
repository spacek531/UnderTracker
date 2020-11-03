from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    double_signal = QtCore.pyqtSignal(int)  # double click signal to set worker to new clicked row
    edit_signal = QtCore.pyqtSignal(int, str)  # send edited system to worker if changed
    next_jump_signal = QtCore.pyqtSignal(bool)

    def __init__(self, hub):
        super(MainWindow, self).__init__()
        self.hub = hub
        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.MainTable = QtWidgets.QTableWidget(self.centralwidget)
        self.spin_delegate = SpinBoxDelegate()
        self.double_spin_delegate = DoubleSpinBoxDelegate()

        self.change_action = QtWidgets.QAction("Edit", self)
        self.save_action = QtWidgets.QAction("Save route", self)
        self.copy_action = QtWidgets.QAction("Copy", self)
        self.new_route_action = QtWidgets.QAction("Start a new route", self)
        self.settings_action = QtWidgets.QAction("Settings", self)
        self.about_action = QtWidgets.QAction("About", self)

        self.last_index = 0

        self.setup_ui()

    def setup_ui(self):
        # connect and add actions
        self.connect_signals()
        # set context menus to custom
        self.MainTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        # build table
        self.MainTable.setGridStyle(QtCore.Qt.NoPen)
        self.MainTable.setColumnCount(4)
        for i in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.MainTable.setHorizontalHeaderItem(i, item)

        self.MainTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.MainTable.setAlternatingRowColors(True)
        self.MainTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.MainTable.verticalHeader().setVisible(False)

        header = self.MainTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        header.setHighlightSections(False)
        header.disconnect()

        self.MainTable.setItemDelegateForColumn(1, self.double_spin_delegate)
        self.MainTable.setItemDelegateForColumn(2, self.double_spin_delegate)
        self.MainTable.setItemDelegateForColumn(3, self.spin_delegate)

        self.gridLayout.addWidget(self.MainTable, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        p = self.MainTable.palette()
        p.setColor(QtGui.QPalette.Highlight, QtGui.QColor(255, 255, 255, 0))
        p.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 123, 255))
        self.MainTable.setPalette(p)
        self.retranslateUi()

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
        self.hub.quit(self.saveGeometry())