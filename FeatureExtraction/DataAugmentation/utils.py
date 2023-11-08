import os

def getFiles(directory_path, recursion=True):
    """
    directory_path: 要获取文件名的目录
    recursion: 是否需要递归搜索，默认为True，会进行递归搜索
    """
    file_list = []
    # 遍历当前目录下的文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            file_list.append(file_path)
        elif os.path.isdir(file_path) and recursion:
            # 如果是子目录，递归调用该函数
            file_list.extend(getFiles(file_path, recursion))
    return file_list
