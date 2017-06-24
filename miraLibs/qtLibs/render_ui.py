# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.osLibs import get_parent_win
from miraFramework.PipelineBaseUI import PipelineBaseUI


def render(widget_class):
    parent_win = get_parent_win.get_parent_win()
    if parent_win:
        global pb_ui
        try:
            pb_ui.close()
            pb_ui.deleteLater()
        except:pass
        pb_ui = PipelineBaseUI(widget_class, parent_win)
        pb_ui.show()
    else:
        import sys
        app = QApplication(sys.argv)
        pb_ui = PipelineBaseUI(widget_class)
        pb_ui.show()
        sys.exit(app.exec_())
