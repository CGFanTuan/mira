# -*- coding: utf-8 -*-
import os
import logging
import sys
import miraCore
from PySide import QtGui
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraScripts.pipeTools.preflight import check_gui
from miraLibs.pipeLibs.pipeMaya import screen_shot, save_as_next_version_file
from miraLibs.mayaLibs import get_scene_name, get_maya_win
from miraLibs.pipeLibs.copy import Copy
from miraFramework.FileListWidget import FileListWidget


maya_window = get_maya_win.get_maya_win("PySide")


class OtherDialog(QtGui.QDialog):
    def __init__(self, other_dir=None, parent=None):
        super(OtherDialog, self).__init__(parent)
        self.other_dir = other_dir
        self.setup_ui()
        self.set_signals()

    def set_signals(self):
        self.submit_btn.clicked.connect(self.do_submit)

    def setup_ui(self):
        self.resize(600, 400)
        self.setWindowTitle("Submit Others")
        self.label = QtGui.QLabel()
        self.label.setText("<font size=4 color=#ff8c00><b>Drag files below:</b></font>")
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.file_list = FileListWidget()
        submit_layout = QtGui.QHBoxLayout()
        self.submit_btn = QtGui.QPushButton("Submit")
        submit_layout.addStretch()
        submit_layout.addWidget(self.submit_btn)
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(submit_layout)
        main_layout.addWidget(self.progress_bar)

    def do_submit(self):
        files = self.file_list.all_items_text()
        if not files:
            self.close()
            return
        self.progress_bar.show()
        self.progress_bar.setRange(0, len(files))
        for index, f in enumerate(files):
            base_name = os.path.basename(f)
            to_other_path = join_path.join_path2(self.other_dir, base_name)
            Copy.copy(f, to_other_path)
            self.progress_bar.setValue(index+1)
        self.close()


class ProgressDialog(QtGui.QProgressDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setRange(1, 100)
        self.setWindowTitle("QCPublish")
        # self.setWindowModality(QtCore.Qt.WindowModal)
        self.setMinimumWidth(600)
        self.canceled.connect(break_down)

    def set_text(self, label_text):
        self.setLabelText(label_text)

    def set_value(self, value):
        self.setValue(value)
        
    def show_up(self):
        self.set_value(10)
        self.show()


def break_down():
    raise Exception("Exit.")


def qcpublish_screen_shot(path_type, image_path):
    if path_type == "asset":
        screen_shot_object = screen_shot.ScreenShot(image_path, False)
        screen_shot_object.screen_shot()
    else:
        return
        # screen_shot_object = screen_shot.ScreenShot(image_path, True)
    # screen_shot_object.screen_shot()


def qcpublish(category):
    script_dir = miraCore.get_scripts_dir()
    publish_dir = join_path.join_path2(script_dir, "pipeTools", "QCPublish")
    if publish_dir not in sys.path:
        sys.path.insert(0, publish_dir)
    category_publish = "{0}_qcpublish".format(category)
    cmd_text = "import {0}; reload({0}); {0}.{0}()".format(category_publish)
    exec(cmd_text)


def is_local_file(path):
    current_project = os.path.basename(path).split("_")[0]
    local_dir = pipeMira.get_local_root_dir(current_project)
    driver = os.path.splitdrive(path)[0]
    if local_dir != driver:
        return False
    else:
        return True


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    message_box = QtGui.QMessageBox.information(None, "Warming Tip", "Do you want to publish this task.",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
    if message_box.name == "No":
        return
    # check is local file
    scene_name = get_scene_name.get_scene_name()
    if not is_local_file(scene_name):
        QtGui.QMessageBox.warning(None, "Warning", "This file is not a local work file.\n Permission defined.")
        return
    # check if work file
    try:
        obj = pipeFile.PathDetails.parse_path(scene_name)
    except:
        logger.warning("Name Error.")
        return
    if not obj.is_working_file():
        QtGui.QMessageBox.warning(None, "Warning", "This file is not a work file.")
        return
    progress_dialog = ProgressDialog(maya_window)
    progress_dialog.show_up()
    # preflight
    progress_dialog.set_text("Preflight checking...")
    result, cg = check_gui.main_for_publish()
    if result:
        cg.close()
    else:
        logger.error("Some checks can not be passed.")
        progress_dialog.close()
        return
    progress_dialog.set_value(30)
    # save as next version file
    saved_scene_name = save_as_next_version_file.save_as_next_version_file(scene_name)
    logger.info("Save to %s" % saved_scene_name)
    progress_dialog.set_value(40)
    # get path
    obj = pipeFile.PathDetails.parse_path(saved_scene_name)
    project = obj.project
    path_type = obj.path_type
    image_path = obj.image_path
    local_image_path = obj.local_image_path
    category = obj.category
    other_dir = obj.other_dir
    # copy to _other
    od = OtherDialog(other_dir, maya_window)
    od.exec_()
    progress_dialog.set_value(50)
    logger.info("Copy to others")
    # screen shot
    progress_dialog.set_text("Screen shot")
    qcpublish_screen_shot(path_type, local_image_path)
    Copy.copy(local_image_path, image_path)
    logger.info("PreQCPublish successful.")
    progress_dialog.set_value(60)
    # post publish
    progress_dialog.set_text("%s_QCPublish" % category)
    qcpublish(category)
    logger.info("QCPublish successful.")
    progress_dialog.set_value(85)
    # write root task id to database
    progress_dialog.set_text("Add to database.")
    logger.info("PostQCPublish successful.")
    # pop message
    progress_dialog.set_value(100)
    QtGui.QMessageBox.information(maya_window, "Warming Tip", "QC publish successful.")


if __name__ == "__main__":
    pass
