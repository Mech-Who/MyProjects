import json
from pprint import pprint
from beeprint import pp

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt, Slot, Signal


class JsonTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        QTreeWidgetItem.__init__(self, parent)

    def setKey(self, key):
        self.setText(0, str(key))

    def getKey(self):
        return self.text(0)

    def setValue(self, value):
        self.setText(1, str(value))

    def getValue(self):
        return self.text(1)

    def setType(self, t):
        self.setText(2, str(t))

    def getType(self):
        return self.text(2)

    def setJsonData(self, json_dict: dict):
        """
        修改给定的json内容中相应的数据
        :param json: 要修改的json内容
        """
        data = self.getValue()
        # 如果类型与值不符合则转换,主要是str转int和float
        if self.getType() == "int" or self.getType() == "float":
            data = eval(f"{self.getType()}(data)")
        # 记录所有的父节点
        parents = []
        p = self.parent()
        while p is not None:
            parents.insert(0, p)
            p = p.parent()
        # 生成索引
        index = ""
        for pa in parents:
            index += f"['{pa.getKey()}']"
        index = f"json_dict{index}['{self.getKey()}']"
        try:
            exec(f"{index} = data")
            print(f"right index: {index}")
        except Exception as e:
            print(f"\033[1;31m error index: {index} \033[0m", e)

    def printContent(self):
        print("key: ", self.text(0), "value: ", self.text(1))


class JsonTreeWidget(QTreeWidget):
    jsonChanged = Signal(dict)
    notInit = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_path = None
        self.json = None
        self.setColumnCount(3)
        self.setHeaderLabels(["Key", "Value", "Type"])
        self.itemChanged.connect(self.changeJson)

    @Slot(JsonTreeWidgetItem, int)
    def changeJson(self, item: JsonTreeWidgetItem, column: int):
        if self.notInit:
            return
        if column == 0 or column == 2:
            return
        item.setJsonData(self.json)
        if self.json_path is not None:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.json, f, indent=2, ensure_ascii=False)
        self.jsonChanged.emit(self.json)

    def setJson(self, jsons: dict | str):
        if isinstance(jsons, str):
            self.json_path = jsons
            with open(jsons, "r", encoding="utf-8") as f:
                self.json = json.load(f)
        elif isinstance(jsons, dict):
            self.json = jsons
        else:
            raise TypeError("Parameter 'jsons' must be dict or str")
        self.setTable(self.json, self)
        self.notInit = False

    def resetJson(self):
        self.clear()
        self.notInit = True

    def getJson(self):
        return self.json

    def setTable(self, json_dict: dict, parent: QTreeWidgetItem | QTreeWidget = None) -> None:
        """
        根据提供的json内容，递归设置JsonTreeWidget内容
        :param json_dict: 提供的json内容
        :param parent: 根据父节点是TreeWidgetItem还是Widget来调用不同的添加子节点方法
        """
        for key, value in json_dict.items():
            item = JsonTreeWidgetItem(parent)
            item.setKey(key)
            # 设置节点value
            if isinstance(value, dict):
                item.setValue("{}")
                item.setType(type(value).__name__)
                self.setTable(value, item)
            elif isinstance(value, list):
                item.setValue("[]")
                item.setType(type(value).__name__)
                for id, i in enumerate(value):
                    childItem = JsonTreeWidgetItem(item)
                    childItem.setKey(id)
                    if isinstance(i, dict):
                        childItem.setValue("{}")
                        childItem.setType(type(i).__name__)
                        self.setTable(i, childItem)
                    else:
                        childItem.setValue(i)
                        childItem.setType(type(i).__name__)
                        childItem.setFlags(childItem.flags() | Qt.ItemIsEditable)
                    item.addChild(childItem)
            else:
                item.setValue(value)
                item.setType(type(value).__name__)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
            # 添加到父节点
            if isinstance(parent, JsonTreeWidget):
                parent.addTopLevelItem(item)
            else:
                parent.addChild(item)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    tree = JsonTreeWidget()
    tree.setWindowTitle("JsonTreeWidget")
    # with open("./test.json", "r", encoding="utf-8") as f:
    #     content = json.load(f)
    # content = content["system_models"][6]
    tree.setJson("./tests/test.json")
    tree.show()
    app.exec()
