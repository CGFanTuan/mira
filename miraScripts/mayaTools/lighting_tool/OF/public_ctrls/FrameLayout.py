__author__ = 'heshuai'


from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class FrameLayout(QGridLayout):

    def __init__(self, button_text=None, collapse_status=None, parent=None):
        super(FrameLayout, self).__init__(parent)
        self.setSizeConstraint(QLayout.SetFixedSize)
        self.setVerticalSpacing(0)
        self.collapse_status = collapse_status
        self.button_text = button_text
        self.tool_btn = QToolButton()
        self.tool_btn.setFixedWidth(380)
        self.tool_btn.setText(self.button_text)
        self.tool_btn.setIconSize(QSize(6, 6))
        self.tool_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.addWidget(self.tool_btn, 0, 0)
        self.addWidget(self.frame, 1, 0)
        self.set_collapse(self.collapse_status)
        self.set_signals()
    
    def set_signals(self):
        self.tool_btn.clicked.connect(self.change_collapse)
        
    def change_collapse(self):
        self.collapse_status = not self.collapse_status
        self.set_collapse(self.collapse_status)

    def set_collapse(self, value):
        ########type(value) == 'bool'
        if value:
            self.collapse_status = True
            self.tool_btn.setArrowType(Qt.RightArrow)
            self.frame.setHidden(True)
        else:
            self.collapse_status = False
            self.tool_btn.setArrowType(Qt.DownArrow)
            self.frame.setHidden(False)


class FrameWidget(QWidget):
    def __init__(self, parent=None):
        super(FrameWidget, self).__init__(parent)
        self.layout = FrameLayout(None, None, self)