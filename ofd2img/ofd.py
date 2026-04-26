#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: F:\code\ofd2img\ofd2img
# CREATE_TIME: 2023-10-07
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: reno
# note:  ofd 基础类
import base64
import os
from io import BytesIO
from typing import Union

import fitz

from PIL import Image
from loguru import logger

from ofd2img.parser_ofd import OFDParser
from ofd2img.draw import DrawPDF, OFDWrite


class OFD(object):
    """ofd对象"""

    def __init__(self, ):
        self.data = None

    def read(self, ofd_f: Union[str, bytes, BytesIO], fmt="b64", save_xml=False, xml_name="testxml"):
        """_summary_
        Args:
            file (_type_): _description_
            fomat (str, optional): _description_. Defaults to "path".
            fomat in ("path","b64","binary")
        """
        if fmt == "path":
            with open(ofd_f, "rb") as f:
                ofd_f = str(base64.b64encode(f.read()), encoding="utf-8")
        elif fmt == "b64":
            pass
        elif fmt == "binary":
            ofd_f = str(base64.b64encode(ofd_f), encoding="utf-8")
        elif fmt == "io":
            ofd_f = str(base64.b64encode(ofd_f.getvalue()), encoding="utf-8")
        else:
            raise "fomat Error: %s" % fmt

        self.data = OFDParser(ofd_f)(save_xml=save_xml, xml_name=xml_name)

    def save(self, ):
        """
        draw ofd xml
        初始化一个xml 文件
        self.data > file
        """
        assert self.data, f"data is None"

    def pdf2ofd(self, pdfbyte, optional_text=False):
        """pdf转ofd"""
        assert pdfbyte, f"pdfbyte is None"
        logger.info(f"pdf2ofd")
        ofd_byte = OFDWrite()(pdfbyte, optional_text=optional_text)
        return ofd_byte

    def to_pdf(self, ):
        """return ofdbytes"""

        assert self.data, f"data is None"
        logger.info(f"to_pdf")
        return DrawPDF(self.data)()

    def pdf2img(self, pdfbytes):

        image_list = []

        doc = fitz.open(stream=pdfbytes, filetype="pdf")

        for page in doc:
            rotate = int(0)
            zoom_x, zoom_y = 1.6, 1.6
            zoom_x, zoom_y = 2, 2
            mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            # 确保使用 RGB 颜色模式，而不是灰度模式 好像没有用
            # 显式设置 colorspace 为 RGB，确保图片是彩色的
            # pix = page.get_pixmap(matrix=mat, alpha=False, colorspace=fitz.csRGB, clip=None, dpi=300, annots=True)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            # 确保使用 RGB 模式创建 PIL 图像
            pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # 强制转换为 RGB 模式，确保颜色正确 好像没有用
            # 检查图像模式，确保是 RGB
            # if pil_image.mode != "RGB":
            #     pil_image = pil_image.convert("RGB")

            # image = np.ndarray((pix.height, pix.width, 3), dtype=np.uint8, buffer=pix.samples)
            # print(image.shape)
            # print(image[2])
            image_list.append(pil_image)
        logger.info(f"pdf2img")
        return image_list

    def jpg2ofd(self, imglist: list):
        """
        imglist: pil image list
        """
        ofd_byte = OFDWrite()(pil_img_list=imglist)
        return ofd_byte

    def jpg2pfd(self, imglist: list):
        """
        imglist: PIL image list
        1 构建data 
        2 DrawPDF(self.data)()
        """

        data = OFDParser(None).img2data(imglist)
        return DrawPDF(data)()

    def to_jpg(self, format="jpg"):
        """
        return pil list
        """
        assert self.data, f"data is None"
        image_list = []
        pdfbytes = self.to_pdf()
        image_list = self.pdf2img(pdfbytes)
        return image_list

    def del_data(self, ):
        """销毁self.data"""
        self.data = None

    def __del__(self):
        del self

    def disposal(self, ):
        """销毁对象"""
        self.__del__()


if __name__ == "__main__":
    ofd = OFD()
