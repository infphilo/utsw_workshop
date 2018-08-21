#!/usr/bin/env python
import sys
from datetime import datetime, date, time

def selectSort(numbers):
    for i in xrange(len(numbers)):
        minIndex = i
        for j in xrange(i+1, len(numbers)):
            if numbers[j] < numbers[minIndex]:
                minIndex = j
        numbers[i], numbers[minIndex] = numbers[minIndex], numbers[i]


def checkSorted(numbers):
    for i in xrange(0, len(numbers) - 1):
        if numbers[i] > numbers[i+1]:
            return False
    return True


if __name__ == "__main__":
    max_num = 1000000

    numbers = range(0, max_num)
    numbers = numbers[::-1]

    print "sorting starts."
    start = datetime.now()
    
    # selectSort(numbers)
    numbers = sorted(numbers)

    print "sorting ends."
    stop = datetime.now()

    duration = (stop - start).total_seconds()
    print "duration:", duration, "seconds"

    passed = checkSorted(numbers)
    if passed:
        print "Correctly sorted."
    else:
        print "Error: numbers are not sorted."
            
