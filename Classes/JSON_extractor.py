from data_extractor import DataExtractor
import pandas as pd

class JSONExtractor(DataExtractor):
    def extract(self, file_path):
        return pd.read_json(file_path)
