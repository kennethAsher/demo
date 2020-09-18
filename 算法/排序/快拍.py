'''
选取中间的66作为基准值（基准值可以随便选）

数列从第一个元素11开始和基准值66进行比较，小于基准值，那么将它放入左边的分区中，第二个元素99比基准值66大，把它放入右边的分区中。

然后依次对左右两个分区进行再分区，直到最后只有一个元素

分解完成再一层一层返回，返回规则是：左边分区+基准值+右边分区
'''

def quick_sort(arr):
    if len(arr) < 2:
        return arr
    mid = arr[len(arr)/2]
    left, right = [],[]
    arr.remove(mid)
    for item in arr:
        if item < mid:
            left.append(item)
        else:
            right.append(item)
    return quick_sort(left) + mid + quick_sort(right)