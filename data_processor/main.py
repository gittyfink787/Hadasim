# main.py

import time
from from processors.file_processor import ExcelProcessor.file_processor import ExcelProcessor
from processors.average_calculator import AvgDataStream

if __name__ == "__main__":
    fp = ExcelProcessor(r"C:\Users\The user\Documents\...path...\time_series.xlsx")
    obj = AvgDataStream(fp)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping")
        del obj
