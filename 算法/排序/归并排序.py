'''
将序列分成n/2的子序列，然后在分成两个子序列，知道每个子序列只有一个值，然后对最后一层分好的子序列排序
然后在对上一层子序列排序
只至将所有的序列都排序完成
'''

def merge_sort(arr):
    if len(arr) == 1:
        return arr
    mid = len(arr) / 2
    left = arr[:mid]
    right = arr[mid:]
    return marge(merge_sort(left), merge_sort(right))

def marge(left, right):
    result = []
    while len(left)>0 and len(right)>0:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result += left
    result += right
    return result