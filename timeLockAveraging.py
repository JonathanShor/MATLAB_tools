import numpy as np
import xlrd
from glob import glob

# Frame(s) to average around. Return array will have same length.
TIMELOCK_FRAMES = [500, 600, 700, 800, 900]
# Width of window. Use an odd number for symmetrical pre- and post- trace lengths.
WINDOW = 61


def collectFiles(filePattern):
    return glob(filePattern, recursive=True)


def findSheet(workbook, metric):
    return workbook.sheet_by_index(0)


def extractFromExcel(excelFile, metric="Mean intensity"):
    """Grab all trace data from excelFile

    Arguments:
        excelFile {str} -- Path to excel file to extract from.

    Keyword Arguments:
        metric {str} -- Extracts from first tab that matches metric.  (default: {"Mean
            intensity"})

    Returns:
        np.ndarray -- Traces by frames.
    """
    workbook = xlrd.open_workbook(excelFile)
    sheet = findSheet(workbook, metric)
    traces = np.empty((sheet.ncols - 1, sheet.nrows - 1))
    for i_trace in range(1, sheet.ncols):
        traces[i_trace - 1, :] = sheet.col_values(i_trace)[1:]
    return traces


def getWindow(trace, centerFrame, width=WINDOW):
    """Get window of size width centered at centerFrame from trace.

        Any window positions outside the bounds of trace set to np.nan.

    Arguments:
        trace {sequence} -- The trace sequence to pull the window from.
        centerFrame {int} -- Index of trace entry to center window around.

    Keyword Arguments:
        width {int} -- Size of window (default: {WINDOW})
    """
    window = np.full((1, width), np.nan)
    startWindowIdx = 0
    endWindowIdx = width
    startTraceIdx = centerFrame - int(width / 2)
    if startTraceIdx < 0:
        startWindowIdx -= startTraceIdx
        startTraceIdx -= startTraceIdx
    endTraceIdx = centerFrame + int(width / 2) + (width % 2)
    if endTraceIdx > len(trace) - 1:
        overshoot = endTraceIdx - (len(trace) - 1)
        endWindowIdx -= overshoot
        endTraceIdx -= overshoot
    window[0, startWindowIdx:endWindowIdx] = trace[startTraceIdx:endTraceIdx]
    return window


def main(filePattern="*.xls*"):
    fileNames = collectFiles(filePattern)

    traceSums = np.zeros((len(TIMELOCK_FRAMES), WINDOW))
    traceCounts = np.zeros(traceSums.shape)
    # averageTraces = np.zeros((TIMELOCK_FRAMES, WINDOW))
    for fileName in fileNames:
        fullTraces = extractFromExcel(fileName)
        for fullTrace in fullTraces:
            for i_timelock, timelock_frame in enumerate(TIMELOCK_FRAMES):
                window = getWindow(fullTrace, timelock_frame, WINDOW)
                traceSums[i_timelock, :] = np.nansum(
                    np.vstack((traceSums[i_timelock, :], window)), axis=0
                )
                traceCounts[i_timelock, :] += ~np.isnan(window)[0, :]

    averageTraces = traceSums / traceCounts
    return averageTraces


if __name__ == "__main__":
    main()
