import time
import numpy as np
import random
import altair as alt
import pandas as pd

data = pd.DataFrame(columns=["method", "size", "time"])

def timer(f):
    def replacement(*args):
        start = time.time_ns()
        result = f(args[0])
        timeTaken = time.time_ns() - start
        return (result, timeTaken/10**9)
    return replacement

@timer
def noRepeatShuffle(array):
    if len(array) < 2:
        raise ValueError("One can't derange an array of size < 2.")
    newArray = list(np.zeros(len(array), dtype=int))
    unused = list(np.arange(0, len(array), 1))
    i = 0
    while True:
        if not unused:
            break
        if len(unused) == 1:
            index = random.randint(0, unused[0]-1)
            unused.pop(0)
        elif unused[0] == i:
            unused.pop(0)
            index = unused[random.randint(0, len(unused)-1)]
            unused.remove(index)
        newArray[i] = array[index]
        newArray[index] = array[i]
        i += 1
    return newArray

@timer
def derangement(array):
    if len(array) < 2:
        raise ValueError("One can't derange an array of size < 2.")
    new = array[:]
    while True:
        random.shuffle(new)
        if isDerangement(array, new):
            return new

def isDerangement(original, new):
    original = np.array(original)
    new = np.array(new)
    return all(original != new)

def record(method, size, time):
    global data
    data = data.append(pd.DataFrame({"method" : [method], "size" : [size], "time" : [time]}), ignore_index=True)

def test(size):
    testArray = list(range(0, size))
    derangement(testArray)[1]
    record("Multiple shuffles", size, derangement(testArray)[1])
    record("Modified index shuffling", size, noRepeatShuffle(testArray)[1])

def testIterations(size, iterationsLeft):
    while iterationsLeft:
        test(size)
        iterationsLeft -= 1

def testSizesUpTo(start, end, step, iterations):
    for size in range(start, end+step, step):
        testIterations(size, iterations)

def graph():
    grouped = data.groupby(["size", "method"]).mean()
    prepped = grouped.reset_index(level="size").reset_index(level="method")
    chart = alt.Chart(prepped).mark_line().encode(
        x="size",
        y="time",
        color="method"
    ).properties(
        width=1584,
        height=960
    ).interactive()
    chart.serve()

if __name__ == "__main__":
    testSizesUpTo(10, 4000, 50, 5)
    graph()