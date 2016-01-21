from bisect import bisect_left

class NumOperation():

    def takeClosest(myList, myNumber):
        """
        Assumes myList is sorted. Returns closest value to myNumber.

        If two numbers are equally close, return the smallest number.
        """
        pos = bisect_left(myList, myNumber)
        if pos == 0:
            return [myList[0],0]
        if pos == len(myList):
            return [myList[-1], len(myList)-1]
        before = myList[pos - 1]
        after = myList[pos]
        if after - myNumber < myNumber - before:
           return [after, pos]
        else:
           return [before, pos - 1]
