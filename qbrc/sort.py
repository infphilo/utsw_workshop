#!/usr/bin/env python
import sys
from datetime import datetime, date, time

def selectSort(numbers, begin, end):
    for i in xrange(begin, end):
        minIndex = i
        for j in xrange(i+1, end):
            if numbers[j] < numbers[minIndex]:
                minIndex = j
        numbers[i], numbers[minIndex] = numbers[minIndex], numbers[i]


def mergeSort(numbers, begin, end, temp):
    None


if __name__ == "__main__":
    sanity_check = True
    
    max_num = 1000000

    numbers = 1:maxnum
    numbers = numbers[::-1]

    print "sorting starts."
    start = datetime.now()
    
    selectSort(numbers, 0, len(numbers))

    print "sorting ends."
    stop = datetime.now()

    duration = (stop - start).total_seconds()
    print "duration:", duration, "seconds"

    if sanity_check:
        passed = checkSorted(numbers)
        if passed:
            print "Correctly sorted."
        else:
            print "Error: numbers are not sorted."
            

