import os

def getFiles(directory_path):
    file_list = []
    # 遍历当前目录下的文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            file_list.append(file_path)
        elif os.path.isdir(file_path):
            # 如果是子目录，递归调用该函数
            file_list.extend(getFiles(file_path))
    return file_list
