from win32com.client import Dispatch, DispatchEx, gencache
import os

'''
转换xls为xlsx格式
'''
def xls2xlsx(xlsPath):
    """
    :param xlsPath: xls文件路径
    :return: 无
    """
    # excelApp = DispatchEx("Excel.Application")
    excelApp = Dispatch("Excel.Application")
    # 设置word不显示
    excelApp.Visible = 0
    excelApp.DisplayAlerts = 0
    xlsxPath = os.path.splitext(xlsPath)[0] + ".xlsx"
    xls = excelApp.Workbooks.Open(xlsPath)
    xls.SaveAs(xlsxPath, 51)
    xls.Close()
    excelApp.Quit()

def xls2xlsx_batch(dir):
    '''
    :param dir: 文件夹路径
    :return: 无
    '''
    files = os.listdir(dir)
    for file_name in files:
        if file_name.rsplit('.',1)[-1]=='xls':
            xls2xlsx(file_name)
