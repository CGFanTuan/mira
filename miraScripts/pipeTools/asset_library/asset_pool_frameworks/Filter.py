# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui, QtCore
from ..asset_pool_libs.get_icon_dir import get_icon_dir


class ButtonLineEdit(QtGui.QLineEdit):

    def __init__(self, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        icon_dir = get_icon_dir()
        self.icon_file = os.path.join(icon_dir, "search.png").replace("\\", "/")
        self.button = QtGui.QToolButton(self)
        self.button.setEnabled(False)
        self.button.setIcon(QtGui.QIcon(self.icon_file))
        self.button.setStyleSheet("QToolButton{border: 0px; padding: 0px; background:transparent}"\
                                  "QToolButton::hover{background:transparent}")
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.editingFinished)

        frame_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        button_size = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (button_size.width() + frame_width + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), button_size.width() + frame_width*2 + 2),
                            max(self.minimumSizeHint().height(), button_size.height() + frame_width*2 + 2))

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().bottom() - button_size.height() + 1)/2)
        super(ButtonLineEdit, self).resizeEvent(event)


if __name__ == "__main__":
    pass
