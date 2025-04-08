# processors/file_processor.py
from abc import ABC, abstractmethod
import os
import pandas as pd


class FileProcessor(ABC):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"The file in {self.path} did not found.")
        self.file = None

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def readlines(self, pos):
        pass

    def get_size(self):
        return os.path.getsize(self.path)

    def get_lines_from_df(self, df, pos):
        if df is None or df.empty or pos >= len(df):
            return []
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        new_rows = df.iloc[pos:]
        return [(row['timestamp'], row['value']) for _, row in new_rows.iterrows()]


class ExcelProcessor(FileProcessor):
    def read(self):
        return pd.read_excel(self.path)

    def write(self):
        return pd.to_excel(self.path)

    def readlines(self, pos):
        df = self.read()
        return self.get_lines_from_df(df, pos)


class ParquetProcessor(FileProcessor):
    def read(self):
        return pd.read_parquet(self.path)

    def write(self):
        return pd.to_parquet(self.path)

    def readlines(self, pos):
        df = self.read()
        return self.get_lines_from_df(df, pos)
