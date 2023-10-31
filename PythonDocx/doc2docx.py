import os.path
from win32com.client import Dispatch, DispatchEx

"""
转换doc为docx格式
"""
def doc2docx(docPath):
    """
    :param docPath: doc文件路径
    :return: 无
    """
    # wordApp = DispatchEx("Word.Application")
    wordApp = Dispatch("Word.Application")
    # 设置word不显示
    wordApp.Visible = 0
    wordApp.DisplayAlerts = 0
    docxPath = os.path.splitext(docPath)[0] + ".docx"
    doc = wordApp.Documents.Open(docPath)
    doc.SaveAs(docxPath, 12, False, "", True, "", False, False, False, False)
    doc.Close()
    wordApp.Quit()

def doc2docx_batch(dir):
    '''
    :param dir: 文件夹路径
    :return: 无
    '''
    files = os.listdir(dir)
    for file_name in files:
        if file_name.rsplit('.',1)[-1]=='doc':
            doc2docx(file_name)