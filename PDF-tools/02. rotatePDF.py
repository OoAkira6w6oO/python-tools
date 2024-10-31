"""
文件名: rotatePDF.py
作者: akira6w6
邮箱: akira6w6@gmail.com
日期: 2024-10-31
描述: 这个 Python 脚本用于将指定 PDF 文件中的每一页旋转 180 度，并将结果覆盖保存到原文件中。其主要功能是读取指定的 PDF 文件，对每一页进行旋转，最后保存修改后的 PDF 文件。

功能概述:
1. 文件检查：脚本首先检查指定路径的 PDF 文件是否存在。如果找不到文件，将提示错误并停止执行。
2. PDF 读取与旋转：
    打开并读取指定的 PDF 文件，创建一个 PyPDF2.PdfReader 对象来获取页面内容。
    使用 PyPDF2.PdfWriter 对象创建新的 PDF 内容。
    遍历 PDF 文件的每一页，调用 rotate 方法将每页旋转 180 度，再将旋转后的页面添加到新的 PDF 写入对象中。
3. 覆盖保存：旋转后的 PDF 内容覆盖原文件，使用相同文件路径保存。

使用说明：
    运行脚本时会提示输入 PDF 文件的绝对路径。
    如果指定的文件存在，脚本将读取并旋转每一页。
    旋转后的 PDF 文件将覆盖原始文件，无需额外文件夹或命名步骤。

注意事项:
- 请确保安装 PyPDF2 库：pip install PyPDF2
- 使用前请备份原文件，以防覆盖操作导致意外修改
"""

import PyPDF2
import os

def rotate_pdf(input_pdf_path):
    # 检查输入PDF文件是否存在
    if not os.path.isfile(input_pdf_path):
        raise FileNotFoundError(f"未找到文件: {input_pdf_path}")

    # 创建一个PDF阅读对象
    with open(input_pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        # 遍历每一页并旋转180度
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.rotate(180)  # 旋转180度
            pdf_writer.add_page(page)

        # 保存旋转后的PDF文件
        output_pdf_path = input_pdf_path  # 覆盖原始文件
        with open(output_pdf_path, "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)

    print(f"文件已旋转180度并保存为: {output_pdf_path}")

if __name__ == "__main__":
    # 提示用户输入PDF文件的绝对路径
    input_pdf_path = input("请输入要旋转的PDF文件的绝对路径: ")

    try:
        rotate_pdf(input_pdf_path)
    except Exception as e:
        print(f"发生错误: {e}")
