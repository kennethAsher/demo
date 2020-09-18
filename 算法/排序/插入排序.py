'''
提出第一个元素，
再取后面的元素依次倒叙向前面元素遍历：每次从后面向前面比较，当遇到能够插在中间的数值的时候，将此数值插入
'''

def insert_sort(arr):
    for i in range(1, len(arr)):
        current = arr[i]
        pre_index = i-1
        while pre_index >=0 and arr[pre_index]>=current:
            arr[pre_index+1] = arr[pre_index]
            pre_index -= 1
        arr[pre_index+1] = current
    return arr