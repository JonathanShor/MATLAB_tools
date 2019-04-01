import numpy as np
import xlrd

# Frame(s) to average around. Return array will have same length.
TIMELOCK_FRAMES = [500, 600, 700, 800, 900]
# Width of window. Use an odd number for symmetrical pre- and post- trace lengths.
WINDOW = 61

# def main():
for center in TIMELOCK_FRAMES:
    pass


def collectFiles():
    pass


def findSheet(workbook, metric):
    return workbook.sheet_by_index(0)


def extractFromExcel(excelFile, metric="Mean intensity"):
    workbook = xlrd.open_workbook(excelFile)
    sheet = findSheet(workbook, metric)
    traces = np.empty((sheet.ncols - 1, sheet.nrows - 1))
    for i_trace in range(1, sheet.ncols):
        traces[i_trace, :] = sheet.col_values(i_trace)[1:]
    return traces


# if if __name__ == "__main__":
# main()
