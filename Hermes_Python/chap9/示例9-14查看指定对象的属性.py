class Person(object):
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def show(self):
        print(f'大家好，我叫:{self.name},我今年:{self.age}岁')

# 创建Person类的对象
per=Person('陈梅梅',20) # 创建对象的时候会自动调用__init__方法（）
print(dir(per))

print(per) # 自动调用了__str__方法
