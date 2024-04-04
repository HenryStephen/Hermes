class Student:
    # 类属性：定义在类中，方法外的变量
    school='北京XXX教育'

    # 初始化方法
    def __init__(self,xm,age):# xm,age是方法的参数，是局部变量,xm,age的作用域是整个__init__方法
        self.name=xm  # =左侧是实例属性， xm是局变量  ,将局部变量的值xm赋值给实例属性self.name
        self.age=age # 实例的名称和局部变量的名称可以相同

    # 定义在类中的函数，称为方法，自带一个参数self
    def show(self):
        print(f'我叫:{self.name}，今年:{self.age}岁了')

# 根据“图纸”可以创建出N多个对象
stu=Student('ysj',18)
stu2=Student('陈梅梅',20)
stu3=Student('马丽',21)
stu4=Student('Marry',23) # 等号的右侧都最Student

print(type(stu))
print(type(stu2))
print(type(stu3))
print(type(stu4))

Student.school='派森教育' # 给类的类属性赋值

# 将学生对象存储到列表中
lst=[stu,stu2,stu3,stu4] # 列表中的元素是Student类型的对象
for item in lst: # item是列表中的元素，是Student类型的对象
    item.show() # 对象名打点调用实例方法

