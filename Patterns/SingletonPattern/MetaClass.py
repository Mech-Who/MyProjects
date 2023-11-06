"""
元类：类的类，如int类型的类型是type类型。

类的定义由它的元类决定，
所以当我们用类A创建一个类时，
Python通过A=type(name, bases, dict)创建它。

name是类的名称
base这是基类
dict这是属性变量

现在，如果一个类有一个预定义的元类（名为Metals），
那么Python就会通过A=MetaKls(name, bases, dict)来创建类
"""
class MyInt(type):
    def __call__(cls, *args, **kwds):
        print("***** Here's My int *****", args)
        print("Now do whatever you want with these objeects...")
        return type.__call__(cls, *args, **kwds)


class int(metaclass=MyInt):
    def __init__(self, x, y):
        self.x = x
        self.y = y

i = int(4, 5)


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=MetaSingleton):
    pass


logger1 = Logger()
logger2 = Logger()
print(logger1, logger2)
