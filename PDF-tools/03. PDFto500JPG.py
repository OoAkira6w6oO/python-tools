"""
文件名: rotatePDF.py
作者: akira6w6
邮箱: akira6w6@gmail.com
日期: 2024-10-31
描述: 这个 Python 脚本用于将 PDF 文件中的每一页转换为单独的 JPG 图像文件，并控制输出图像的文件大小不超过指定的最大值（默认 500 KB）。如果 PDF 仅有一页，图像将直接使用原始 PDF 文件的名称；如果是多页文件，生成的文件名将包含页码。

功能概述:
1. 输入文件处理：获取输入 PDF 文件的文件夹路径和文件名，以便在相同目录下保存转换后的 JPG 文件。
2. PDF 转 JPG：
    使用 pdf2image 库的 convert_from_path 方法将 PDF 文件的每一页转换为图像。
    对于每一页，生成对应的 JPG 文件。
3. 文件大小控制：
    默认设置图像质量为 95。
    如果输出 JPG 文件超过指定的最大大小（max_size_kb），则逐步降低质量（每次减少 5）直至符合要求或降到最低质量限制（10%）。
    若无法在指定的文件大小内保持图像质量，会在控制台输出提示。
4. 文件命名：
    单页 PDF 文件的 JPG 文件使用原文件名。
    多页 PDF 文件的 JPG 文件会在文件名后附加页码。

使用说明：
    执行脚本时，将提示用户输入 PDF 文件的绝对路径。
    脚本会自动将 PDF 文件转换为 JPG 格式并保存至同一文件夹中。
    默认大小限制为 500 KB，可以在调用 pdf_to_jpg 函数时修改 max_size_kb 参数。

注意事项:
- 请确保安装 pdf2image 和 Pillow 库：pip install pdf2image pillow
- 该脚本使用了 Ghostscript 来处理 PDF 图像转换，需提前安装并配置路径
"""

import os
from pdf2image import convert_from_path
from PIL import Image

def pdf_to_jpg(input_pdf_path, max_size_kb=500):
    # 获取输入文件夹路径和文件名
    folder_path = os.path.dirname(input_pdf_path)
    base_name = os.path.basename(input_pdf_path).replace('.pdf', '')

    # 将PDF转换为图片
    images = convert_from_path(input_pdf_path)

    # 遍历每一页生成 JPG 文件
    for page_num, image in enumerate(images):
        # 根据页数决定文件名
        if len(images) == 1:
            jpg_path = os.path.join(folder_path, f"{base_name}.jpg")  # 如果只有一页，使用文件名
        else:
            jpg_path = os.path.join(folder_path, f"{base_name}_{page_num + 1}.jpg")  # 多页文件

        # 初始质量设置
        quality = 95
        while True:
            # 保存为 JPG，设置质量
            image.save(jpg_path, 'JPEG', quality=quality)

            # 检查文件大小
            if os.path.getsize(jpg_path) <= max_size_kb * 1024:
                print(f"已保存: {jpg_path}，文件大小: {os.path.getsize(jpg_path) / 1024:.2f} KB")
                break
            else:
                quality -= 5  # 减少质量以减少文件大小
                if quality < 10:  # 防止质量降到太低
                    print(f"无法将文件大小控制在 {max_size_kb} KB，已保存为: {jpg_path}，文件大小: {os.path.getsize(jpg_path) / 1024:.2f} KB")
                    break

if __name__ == "__main__":
    # 提示用户输入PDF文件的绝对路径
    input_pdf_path = input("请输入要转换的PDF文件的绝对路径: ")

    try:
        pdf_to_jpg(input_pdf_path)
    except Exception as e:
        print(f"发生错误: {e}")
