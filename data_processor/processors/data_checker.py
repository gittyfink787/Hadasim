# processors/data_checker.py
from datetime import datetime
import pandas as pd


class CheckData:
    def __init__(self, file_processor):
        self.file_processor = file_processor

    def get_df(self):
        return self.file_processor.read()

    def get_invalid_dates(self):
        df = self.get_df()

        def is_valid_date(date_column):
            try:
                datetime.strptime(str(date_column).strip(), "%Y-%m-%d %H:%M:%S")
                return True
            except ValueError:
                return False

        return df[~df.iloc[:, 0].apply(is_valid_date)]

    def get_duplicated_records(self):
        df = self.get_df()
        return df[df.duplicated()]

    def find_outliners(self):
        df = self.get_df()
        num_value = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        list_value = list(df.iloc[:, 1])

        avg = num_value.mean()
        std = num_value.std()
        ALLOWD_STD = 3

        mask = []
        for val in list_value:
            if (not isinstance(val, (int, float)) or pd.isna(val)
                    or avg - ALLOWD_STD * std < val < avg + ALLOWD_STD * std):
                mask.append(False)
            else:
                mask.append(True)

        return df[mask]
