# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import pipeGlobal
from miraLibs.pyLibs import join_path


class Filter(QLineEdit):

    def __init__(self, icon_file=None, parent=None):
        super(Filter, self).__init__(parent)

        self.icon_file = icon_file
        if not self.icon_file:
            icon_dir = pipeGlobal.icons_dir
            self.icon_file = join_path.join_path2(icon_dir, "search.png")
        self.button = QToolButton(self)
        self.button.setEnabled(False)
        self.button.setIcon(QIcon(self.icon_file))
        self.button.setStyleSheet("QToolButton{border: 0px; padding: 0px; background:transparent}"\
                                  "QToolButton::hover{background:transparent}")
        self.button.setCursor(Qt.ArrowCursor)
        self.button.clicked.connect(self.editingFinished)

        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        button_size = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (button_size.width() + frame_width + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), button_size.width() + frame_width*2 + 2),
                            max(self.minimumSizeHint().height(), button_size.height() + frame_width*2 + 2))

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().bottom() - button_size.height() + 1)/2)
        super(Filter, self).resizeEvent(event)


if __name__ == "__main__":
    pass
