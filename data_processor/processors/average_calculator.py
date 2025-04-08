# processors/average_calculator.py
from abc import ABC, abstractmethod
import os
import pandas as pd
import numpy as np
from datetime import datetime
import threading
import schedule
import time


class CalAverage(ABC):
    def __init__(self, file_processor):
        self.file_processor = file_processor

    @abstractmethod
    def average(self, pathes=None):
        pass


class AvgDividedData(CalAverage):
    def get_df(self):
        return self.file_processor.read()

    def divide_data(self):
        df = self.get_df()
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        pathes = []
        output_dir = "process_data_2"
        os.makedirs(output_dir, exist_ok=True)

        grouped = df.groupby(df['timestamp'].dt.date)

        for date, group in grouped:
            file_name = os.path.join(output_dir, f"data_{date}.csv")
            group.to_csv(file_name, index=False)
            pathes.append(file_name)

        return pathes

    def average(self, pathes):
        total_sum = 0
        total_count = 0

        for path in pathes:
            df = pd.read_csv(path)
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            total_sum += df['value'].sum()
            total_count += df['value'].count()

        return total_sum / total_count

    def divide_and_calc_avg(self):
        return self.average(self.divide_data())


class AvgDataStream(CalAverage):
    def __init__(self, file_processor):
        super().__init__(file_processor)
        self.buffer = []
        self.buffer_lock = threading.Lock()
        self.last_pos = 0
        self.last_count = 0
        self.last_sum = 0

        with open('hourly_update.txt', 'w') as f:
            f.truncate(0)

        self._stop_event = threading.Event()

        self.thread_read = threading.Thread(target=self.watch_file, daemon=True)
        self.thread_read.start()

        self.job = schedule.every().hour.at(":00").do(self.average)
        self.thread_analyze = threading.Thread(target=self.run_schedule, daemon=True)
        self.thread_analyze.start()

    def read_new_data(self):
        print(f"{datetime.now()}: Reading new data")
        curr_pos = self.file_processor.get_size()
        if curr_pos > self.last_pos:
            lines = self.file_processor.readlines(self.last_pos)
            self.last_pos = curr_pos
            return self.write_to_buffer(lines)

    def write_to_buffer(self, lines):
        with self.buffer_lock:
            for line in lines:
                timestamp, value = line[0], line[1]
                self.buffer.append({'timestamp': timestamp, 'value': value})

    def average(self):
        values = []
        with self.buffer_lock:
            if self.buffer:
                values = [d['value'] for d in self.buffer if pd.notna(d['value'])]
                self.buffer.clear()
            else:
                self.write_to_file(None, None)

        curr_count = len(values)
        curr_sum = sum(values)

        if curr_count > 0:
            total_avg = (self.last_sum + curr_sum) / (self.last_count + curr_count)
            last_hour_avg = curr_sum / curr_count
        else:
            total_avg = self.last_sum / self.last_count if self.last_count > 0 else None
            last_hour_avg = None

        self.write_to_file(last_hour_avg, total_avg)

        self.last_count += curr_count
        self.last_sum += curr_sum

    def write_to_file(self, last_hour_avg, total_avg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("hourly_update.txt", 'a') as r:
            if last_hour_avg is not None:
                r.write(f"Analysis at {now}  : Total average: {total_avg}, Last hour average: {last_hour_avg}\n")
            else:
                r.write(f"No data in the last hour at {now} \n")

    def watch_file(self):
        while not self._stop_event.is_set():
            self.read_new_data()
            time.sleep(10)

    def run_schedule(self):
        while not self._stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)

    def __del__(self):
        self._stop_event.set()
        schedule.clear()
