#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OFD 转 JPG 脚本
使用 easyofd 库将 OFD 文件转换为 JPG 图片
"""
import os
import sys
import base64

# 添加 easyofd 库到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "easyofd"))

# 注册系统中可用的中文字体
import subprocess
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError

def register_system_fonts():
    """注册系统中可用的字体到 reportlab"""
    print("正在扫描并注册系统字体...")
    txt = subprocess.getoutput('fc-list :lang=zh', encoding='UTF-8')
    lines = txt.splitlines()
    
    registered_fonts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(":")
        font_file = parts[0].strip()
        if not font_file.lower().endswith('.ttf') and not font_file.lower().endswith('.ttc'):
            continue
        font_names = parts[1].split(",")
        for font_name in font_names:
            font_name = font_name.strip().replace('\\', '')
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_file))
                registered_fonts.append(font_name)
                print(f"成功注册字体: {font_name}")
            except TTFError as err:
                print(f"字体注册失败 - 名称: {font_name}, 文件: {font_file}, 错误: {err}")
    
    print(f"字体注册完成，成功注册 {len(registered_fonts)} 个字体")
    return registered_fonts

# 注册字体
# register_system_fonts()

from easyofd.ofd import OFD

def ofd_to_jpg(ofd_file_path):
    """
    将 OFD 文件转换为 JPG 图片
    :param ofd_file_path: OFD 文件路径
    :return: 生成的 JPG 文件路径列表
    """
    if not os.path.exists(ofd_file_path):
        print(f"错误: 文件 '{ofd_file_path}' 不存在")
        return []
    
    if not ofd_file_path.lower().endswith('.ofd'):
        print(f"错误: 文件 '{ofd_file_path}' 不是 OFD 文件")
        return []
    
    try:
        # 获取文件名前缀
        file_prefix = os.path.splitext(os.path.split(ofd_file_path)[1])[0]
        output_dir = os.path.dirname(ofd_file_path)
        
        # 读取 OFD 文件并转换为 base64
        with open(ofd_file_path, "rb") as f:
            ofdb64 = str(base64.b64encode(f.read()), "utf-8")
        
        # 初始化 OFD 工具类
        ofd = OFD()
        print(f"正在解析 OFD 文件: {ofd_file_path}")
        ofd.read(ofdb64)
        
        # 转换为 JPG
        print("正在转换为 JPG...")
        # 尝试使用系统中可用的字体
        from easyofd.draw.font_tools import FontTool
        font_tool = FontTool()
        print(f"系统可用字体: {font_tool.FONTS}")
        img_np = ofd.to_jpg()
        
        # 保存图片
        output_files = []
        for idx, img in enumerate(img_np):
            output_file = os.path.join(output_dir, f"{file_prefix}_{idx}.jpg")
            img.save(output_file)
            output_files.append(output_file)
            print(f"生成图片: {output_file}")
        
        # 清理数据
        ofd.del_data()
        
        print(f"转换完成，共生成 {len(output_files)} 张图片")
        return output_files
        
    except Exception as e:
        print(f"转换过程中出错: {str(e)}")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python ofd2jpg.py <ofd文件路径>")
        sys.exit(1)
    
    ofd_file = sys.argv[1]
    result = ofd_to_jpg(ofd_file)
    if not result:
        sys.exit(1)
