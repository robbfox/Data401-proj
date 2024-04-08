from data_extractor import DataExtractor
import pandas as pd

class CSVExtractor(DataExtractor):
    def extract(self, file_path):
        return pd.read_csv(file_path)