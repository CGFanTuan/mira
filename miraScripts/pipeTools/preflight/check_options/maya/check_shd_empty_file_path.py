# -*- coding: utf-8 -*-
import pymel.core as pm
from miraLibs.mayaLibs import get_texture_real_path
from BaseCheck import BaseCheck


class check_shd_empty_file_path(BaseCheck):

    def run(self):
        file_nodes = pm.ls(type="file")
        # if has no file nodes ...return
        if not file_nodes:
            self.pass_check("No file node.")
            return
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"file节点的文件路径有误")
        else:
            self.pass_check(u"file节点文件路径正确")

    @staticmethod
    def get_error_list():
        invalid_files = list()
        file_nodes = pm.ls(type="file")
        for file_node in file_nodes:
            tex_path = file_node.computedFileTextureNamePattern.get()
            real_paths = get_texture_real_path.get_texture_real_path(tex_path)
            if not real_paths:
                invalid_files.append(file_node.name())
        return invalid_files

if __name__ == "__main__":
    pass
