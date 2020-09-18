# 首先导入需要的库和路径
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

if __name__ == "__main__":
    # 设置保存pdf文件的文件夹
    dir_path = r'/data/pdf_data/'
    # 设置文件的名字
    file_name = "中华眼科学（第3版）合并版.pdf"

# 获得所有pdf文件的绝对路径，需要os.walk遍历文件
for dirpath, dirs, files in os.walk(dir_path):
    print(dirpath)
    print(files)

# 直接将需要合并的pdf放在一个文件夹下面，这样无需对文件的后缀进行判断了, 包装成函数如下


def GetFileName(dir_path):
    file_list = [os.path.join(dir_path, filesname) for dirpath, dirs, files in os.walk(
        dir_path) for filesname in files]
    return file_list

# 建立合并pdf的函数
def MergePDF(dir_path, file_name):
    output = PdfFileWriter()
    outputPages = 0
    file_list = GetFileName(dir_path)
    for pdf_file in file_list:
        print("文件：%s" % pdf_file.split('\\')[-1], end=' ')
        #读取pdf文件
        input = PdfFileReader(open(pdf_file, "rb"))
        #获得源PDF文件中的页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        print("页数：%d" % pageCount)
    for iPage in range(pageCount):
        output.addPage(input.getPage(iPage))
    print("\n合并后的总页数:%d" % outputPages)
    # 写入到目标PDF文件
    print("PDF文件正在合并，请稍等......")
    with open(os.path.join(dir_path, file_name), "wb") as outputfile:
        # 注意这里的写法和正常的上下文文件写入是相反的
        output.write(outputfile)
    
    print("PDF文件合并完成")



'''
综合代码
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def GetFileName(dir_path):
    file_list = [os.path.join(dirpath, filesname) \
                 for dirpath, dirs, files in os.walk(dir_path) \
                 for filesname in files]
    return file_list

def MergePDF(dir_path, file_name):
    output = PdfFileWriter()
    outputPages = 0
    file_list = GetFileName(dir_path)
    for pdf_file in file_list:
        print("文件：%s" % pdf_file.split('\\')[-1], end=' ')
        # 读取PDF文件
        input = PdfFileReader(open(pdf_file, "rb"))
        # 获得源PDF文件中页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        print("页数：%d" % pageCount)
        # 分别将page添加到输出output中
        for iPage in range(pageCount):
            output.addPage(input.getPage(iPage))
    print("\n合并后的总页数:%d" % outputPages)
    # 写入到目标PDF文件
    print("PDF文件正在合并，请稍等......")
    with open(os.path.join(dir_path, file_name), "wb") as outputfile:
        # 注意这里的写法和正常的上下文文件写入是相反的
        output.write(outputfile)
    print("PDF文件合并完成")

if __name__ == '__main__':
    # 设置存放多个pdf文件的文件夹
    dir_path = r'C:\Scientific Research\Knowladge\Ophthalmology\Chinese Ophthalmology'
    # 目标文件的名字
    file_name = "中华眼科学（第3版）合并版.pdf"
    MergePDF(dir_path, file_name)
'''
