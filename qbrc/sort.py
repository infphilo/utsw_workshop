#!/usr/bin/env python
import sys
from datetime import datetime, date, time

def selectSort(numbers):
    for i in xrange(begin, end):
        minIndex = i
        for j in xrange(i+1, end):
            if numbers[j] < numbers[minIndex]:
                minIndex = j
        numbers[i], numbers[minIndex] = numbers[minIndex], numbers[i]


def checkSorted(numbers):
    for i in xrange(0, len(numbers) - 1):
        if numbers[i] > numbers[i+1]:
            return False
    return True


if __name__ == "__main__":
    sanity_check = True
    
    max_num = 100000

    numbers = range(0, max_num)
    numbers = numbers[::-1]

    print "sorting starts."
    start = datetime.now()
    
    selectSort(numbers)

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
            
