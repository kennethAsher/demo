
'''
遍历数组，设定一个最小值，找出最小的值放在与首位互换位置，以此来进行排序

'''

def selectionsotr(arr):
    for i in range(len(arr)-1):
        minIndex = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        if i != minIndex:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr