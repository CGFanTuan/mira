# -*- coding: utf-8 -*-
import os
from functools import partial
from PySide import QtGui, QtCore
from ..libs.start_file import start_file
from ..libs.get_app_icon import get_app_icon


class AppButton(QtGui.QToolButton):
    def __init__(self, name=None, exe_path=None, parent=None, can_rename=True):
        super(AppButton, self).__init__(parent)
        self.name = name
        self.exe_path = exe_path
        self.parent = parent
        self.can_rename = can_rename
        self.setMaximumHeight(55)
        self.setMaximumWidth(180)
        self.setStyleSheet("QToolButton{background: transparent; border-radius: 5px;}")
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        icon = get_app_icon(self.exe_path)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(100, 100))
        self.set_text()
        self.menu = QtGui.QMenu(self)
        self.remove_action = QtGui.QAction("Remove", self)
        self.rename_action = QtGui.QAction("Rename", self)
        self.launch_action = QtGui.QAction("Launch folder", self)
        self.set_signals()

    def set_text(self):
        elidfont = QtGui.QFontMetrics(self.font())
        text = elidfont.elidedText(self.name, QtCore.Qt.ElideRight, self.width())
        self.setText(text)

    def set_signals(self):
        self.clicked.connect(partial(start_file, self.exe_path))
        self.remove_action.triggered.connect(self.remove_self)
        self.rename_action.triggered.connect(self.rename_self)
        self.launch_action.triggered.connect(self.do_launch)

    def contextMenuEvent(self, event):
        self.menu.clear()
        if self.can_rename:
            self.menu.addAction(self.rename_action)
        self.menu.addAction(self.remove_action)
        self.menu.addAction(self.launch_action)
        self.menu.exec_(QtGui.QCursor.pos())
        event.accept()

    def remove_self(self):
        self.deleteLater()

    def rename_self(self):
        name, ok = QtGui.QInputDialog.getText(self, "App Name", "Please input an app name",
                                              QtGui.QLineEdit.Normal, self.name)
        if name and ok:
            self.name = name
            self.set_text()

    def do_launch(self):
        exe_dir = os.path.dirname(self.exe_path)
        if os.path.isdir(exe_dir):
            start_file(exe_dir)
        else:
            QtGui.QMessageBox.warning(None, "warning", "%s is not an exist directory." % exe_dir)