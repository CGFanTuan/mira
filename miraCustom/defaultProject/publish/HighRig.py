# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, delete
from miraLibs.pipeLibs.pipeMaya import publish, rename_pipeline_shape


def main(file_name, local):
    logger = logging.getLogger("HighRig publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    # copy image
    publish.copy_image_and_video(context)
    logger.info("Copy image and video done.")
    # import all reference
    publish.reference_opt()
    logger.info("Import reference done.")
    # delete blends
    delete.delete("_BLENDS")
    # rename shape
    if not rename_pipeline_shape.rename_pipeline_shape():
        raise RuntimeError("Rename shape error.")
    logger.info("Rename shape done.")
    # export needed
    publish.export_need_to_publish(context, "rig")
    logger.info("Export to publish path done.")
    # quit maya
    if not local:
        quit_maya.quit_maya()
