#冒泡排序：
    #从前向后面遍历，每次遇到前面比后面相邻数值小的情况，此两个值呼唤位置


def bubbleSort(arr):
    for i in range(1,len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j + 1], arr[j]
    return arr
