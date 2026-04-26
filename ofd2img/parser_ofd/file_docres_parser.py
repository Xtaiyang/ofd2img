#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME:  file_docres_parser.py
# CREATE_TIME: 2025/3/28 11:48
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: reno
# NOTE: 解析 DocumentRes

import os

from .file_parser_base import FileParserBase

class DocumentResFileParser(FileParserBase):
    """
    Parser DocumentRes 抽取里面图片信息
    /xml_dir/Doc_0/DocumentRes.xml
    """

    def __call__(self):
        info = {"multi_media": {}, "draw_params": {}}
        multi_media: list = []
        multi_media_key = "ofd:MultiMedia"
        self.recursion_ext(self.xml_obj, multi_media, multi_media_key)
        if multi_media:
            for media in multi_media:
                name = media.get("ofd:MediaFile", "") 
                info["multi_media"][media.get("@ID")] = {
                    "format": media.get("@Format", ""),
                    "wrap_pos": media.get("@wrap_pos", ""),
                    # "Boundary": media.get("@Boundary", ""),
                    "type": media.get("@Type", ""),
                    "suffix": os.path.splitext(name)[-1].replace(".", ""),  # 文件后缀名
                    "fileName": name,
                }
        
        draw_params: list = []
        self.recursion_ext(self.xml_obj, draw_params, "ofd:DrawParam")
        if draw_params:
            for i in draw_params:
                info["draw_params"][i.get("@ID")] = i
        
        return info