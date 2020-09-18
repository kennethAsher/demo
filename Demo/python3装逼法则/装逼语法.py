#01 for else
for i in range(10):
    print(i)
else:
    print(i,'this is else')

#一颗星(*)和两颗星(*)
# 使用一颗*代表参数，单值
def multi_sum(*args):
    s = 0
    for item in args:
        s += item
    return s

k = multi_sum(3,4,5)
print(k)
#两颗*代表键值
def do_somthing(name, age, gender='man', *args, **kwds):
    print(f'name:${name} age:${age} gender:${gender}')
    print(args)
    print(kwds)
do_somthing('zhansan','50','man',15,32,6,math=99)

#列表推导式
a = [1,2,3,4,5]
result = [i*i for i in a]
print(result)

#列表索引骚操作---将推导式标注的地方替换成指定的列表
a = [0,1,2,3,4,5]
b = ['a', 'b']
a[3:6] = b
a[2:2] = b
print(a)


#lambda表达式  lambda x,y:x+y

#例如
a = [{'name': 'B', 'age': 50}, {'name': 'A', 'age': 30}, {'name': 'C', 'age': 40}]
sorted(a, key=lambda x: x['name'])  #按照姓名排序

#求一组数据元素平方的例子
a = [1,2,3]
for item in map(lambda x:pow(x,2), a):
    print(item)


#yield 生成器，迭代器
#批量使用大规模的列表非常占用内存，使用迭代器代替列表，能够节省非常多的内存，
# 生成器是迭代器的一种，他有着遍历一遍就自动消失的属性
# yield是生成迭代器的一种方式

#python内置了iter函数，用于生成迭代器
a = [1,2,3]
a_iter = iter(a)
print(a_iter)  # <list_iterator object at 0x0000011F72FC06D0>
for i in a_iter:
    print(i)

#使用yield构造生成器
def get_square(n):
    for i in range(n):
        yield(pow(i,2)) # 循环yield能够直接返回生成器
a = get_square(5)
print(a)
for i in a:
    print(i)
print(a)
for i in a:
    print(i)

#装饰器
import time
def timer(func):
    def wrapper(*args, **kwds):
        t0 = time.time()
        func(*args, **kwds)
        t1 = time.time()
        print(f'耗时%0.3f' %(t1-t0))
    return wrapper
@timer
def do_somthing(delay):
    print('starting......')
    time.sleep(delay)
    print('end.......')

do_somthing(3)


#使用assert进行调试，当判定结果为true，正常执行，否则，抛出AssertionError
import time
def do_somthing(delay):
    assert(isinstance(delay, (int, float))) , "the args must be int or float"
    print('startint sleep')
    time.sleep(delay)
    print('i am wake up')
do_somthing(2)
do_somthing(1.3)
do_somthing('s') 