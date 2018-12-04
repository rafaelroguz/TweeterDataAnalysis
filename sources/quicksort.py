def quickSort(alist, sort_propertie):
    quickSortHelper(alist, sort_propertie, 0, len(alist) - 1)


def quickSortHelper(alist, sort_propertie, first, last):
    if first < last:
        splitpoint = partition(alist, sort_propertie, first, last)

        quickSortHelper(alist, sort_propertie, first, splitpoint - 1)
        quickSortHelper(alist, sort_propertie, splitpoint + 1, last)


def partition(alist, sort_propertie, first, last):
    pivotvalue = alist[first]

    leftmark = first + 1
    rightmark = last

    done = False
    while not done:
        while leftmark <= rightmark and alist[leftmark][sort_propertie] >= pivotvalue[sort_propertie]:
            leftmark = leftmark + 1

        while alist[rightmark][sort_propertie] <= pivotvalue[sort_propertie] and rightmark >= leftmark:
            rightmark = rightmark - 1

        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp

    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp

    return rightmark


def sort_list(list, field):
    list_to_sort = list
    quickSort(list_to_sort, field)

    return list_to_sort
