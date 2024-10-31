"""
文件名: seperatePDF.py
作者: akira6w6
邮箱: akira6w6@gmail.com
日期: 2024-10-31
描述: 这个 Python 脚本用于将一个 PDF 文件按页分割成多个单页 PDF 文件，并将这些单页文件保存在指定的输出文件夹中。

功能概述:
1. 输入文件检查：脚本首先检查 input.pdf 是否存在于当前目录中，如果不存在则报错并停止执行。
2. 输出文件夹处理：
    脚本会检查指定的输出文件夹 output 是否已存在。
    如果文件夹存在且不为空，脚本会提示用户是否要删除该文件夹及其内容。若用户确认删除，则清空文件夹；若用户拒绝，脚本将取消操作。
    如果文件夹存在且为空，则删除空文件夹。
    然后，脚本会创建一个新的输出文件夹用于存储分割后的 PDF 页面。
3. PDF 分割：
    脚本打开输入的 PDF 文件，并使用 PyPDF2 库读取其页面数。
    逐页读取 PDF，将每一页保存为独立的单页 PDF 文件。
    每个单页 PDF 文件将按照顺序命名为 page_1.pdf、page_2.pdf 等，保存在输出文件夹中。

注意事项:
- 请确保安装 PyPDF2 库：pip install PyPDF2
- 脚本路径中的 input.pdf 文件应放置在脚本的当前目录中，且确保 output 文件夹具有写入权限。
"""

# 代码实现
import PyPDF2
import os
import shutil

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 输入文件路径和输出文件夹路径
input_pdf_path = os.path.join(current_dir, "input.pdf")    # 当前目录下的 input.pdf
output_folder = os.path.join(current_dir, "output")        # 当前目录下的 output 文件夹

def split_pdf(input_pdf_path, output_folder):
    # 检查输入PDF文件是否存在
    if not os.path.isfile(input_pdf_path):
        raise FileNotFoundError(f"未找到文件: {input_pdf_path}")

    # 检查输出文件夹是否存在
    if os.path.exists(output_folder):
        # 检查文件夹是否为空
        if os.listdir(output_folder):
            # 询问用户是否删除
            response = input(f"输出文件夹 {output_folder} 存在且不为空，是否继续删除？ (y/n): ")
            if response.lower() == 'y':
                shutil.rmtree(output_folder)  # 删除文件夹及其内容
                print(f"已删除文件夹: {output_folder}")
            else:
                print("操作已取消。")
                return
        else:
            # 如果文件夹存在且为空，直接删除
            os.rmdir(output_folder)

    # 创建新的输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 打开源PDF文件
    with open(input_pdf_path, "rb") as pdf_file:
        # 创建一个PDF阅读对象
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # 获取总页数
        total_pages = len(pdf_reader.pages)
        
        # 遍历每一页，分别保存
        for page_num in range(total_pages):
            # 创建PDF写入对象
            pdf_writer = PyPDF2.PdfWriter()
            # 添加当前页到PDF写入对象
            pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # 定义单页PDF文件的输出路径
            output_pdf_path = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
            with open(output_pdf_path, "wb") as output_pdf_file:
                pdf_writer.write(output_pdf_file)
            print(f"页面 {page_num + 1} 已保存为 {output_pdf_path}")

# 使用示例
try:
    split_pdf(input_pdf_path, output_folder)
except Exception as e:
    print(f"发生错误: {e}")
