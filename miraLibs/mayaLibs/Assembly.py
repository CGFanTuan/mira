# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
logger = logging.getLogger("Assembly")


class Assembly(object):

    def __init__(self):
        pass

    @staticmethod
    def create_assembly_node(name, typ):
        if typ not in ["assemblyDefinition", "assemblyReference"]:
            logger.error("type is wrong")
            return
        assembly_node = mc.assembly(name=name, type=typ)
        return assembly_node

    @staticmethod
    def get_representation_index(node, rep_name):
        all_representation = mc.assembly(node, q=1, listRepresentations=1)
        if rep_name in all_representation:
            return all_representation.index(rep_name)

    @staticmethod
    def create_representation(node, rep_type, rep_name, rep_label, input_path):
        if not mc.objExists(node):
            logger.error("%s does not exist." % node)
            return
        all_representation = mc.assembly(node, q=1, listRepresentations=1)
        if all_representation and rep_name in all_representation:
            logger.warning("%s in the representation" % rep_name)
            return
        mc.assembly(node, e=1, createRepresentation=rep_type, repName=rep_name, input=input_path)
        all_representation = mc.assembly(node, q=1, listRepresentations=1)
        index = all_representation.index(rep_name)
        if rep_label:
            mc.setAttr("%s.rep[%s].rla" % (node, index), rep_label, type="string")

    def reference_ad(self, name, ad_path):
        ar_node = self.create_assembly_node(name, "assemblyReference")
        mc.setAttr("%s.definition" % ar_node, ad_path, type="string")
        return ar_node

    @staticmethod
    def get_all_ar_nodes(selected=None, include_hide=True):
        if selected:
            selected_objs = mc.ls(sl=1)
            if not selected_objs:
                raise RuntimeError("Selected something")
            sel_ar_nods = mc.listRelatives(selected_objs, ad=1, type="assemblyReference")
            all_nodes = selected_objs + sel_ar_nods
            ar_nodes = mc.ls(all_nodes, type="assemblyReference")
            ar_nodes = list(set(ar_nodes))
        else:
            ar_nodes = mc.ls(type="assemblyReference")
        if not include_hide:
            ar_nodes = [ar_node for ar_node in ar_nodes if mc.getAttr("%s.visibility" % ar_node)]
        return ar_nodes

    def get_all_reps(self, selected=None):
        ar_nodes = self.get_all_ar_nodes(selected)
        if not ar_nodes:
            return
        all_reps = list()
        for node in ar_nodes:
            reps = mc.assembly(node, q=1, listRepresentations=1)
            if not reps:
                continue
            all_reps.extend(reps)
        all_reps = list(set(all_reps))
        return all_reps

    def set_active(self, rep, selected=None, include_hide=True):
        ar_nodes = self.get_all_ar_nodes(selected, include_hide)
        for ar_node in ar_nodes:
            reps = mc.assembly(ar_node, q=1, listRepresentations=1)
            if rep not in reps:
                print "%s not in the representations of node %s" % (rep, ar_node)
                continue
            mc.assembly(ar_node, e=1, activeLabel=rep)
