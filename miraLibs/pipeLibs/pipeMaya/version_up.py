# -*- coding: utf-8 -*-
import os
from PySide import QtGui
import maya.mel as mel
from miraLibs.mayaLibs import save_as
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import get_new_version_by_dir


def version_up():
    obj = pipeFile.PathDetails.parse_path()
    if not obj:
        return
    if not obj.is_local_file():
        print "This file is not a local file."
        return
    next_version_file = obj.next_version_file
    if os.path.isfile(next_version_file):
        ret = QtGui.QMessageBox.information(None, "Save As",
                                            "%s \nalready exists.Do you want to replace it?" % next_version_file,
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if ret.name == "Yes":
            save_as.save_as(next_version_file)
        else:
            try:
                new_version_file = get_new_version_by_dir.get_new_version_by_dir(os.path.dirname(next_version_file))
                save_as.save_as(new_version_file[0])
            except:
                mel.eval("SaveSceneAs;")
    else:
        ret = QtGui.QMessageBox.information(None, "Version up", "Save as %s?" % next_version_file,
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if ret.name == "Yes":
            save_as.save_as(next_version_file)


if __name__ == "__main__":
    pass
