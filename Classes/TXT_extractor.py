from data_extractor import DataExtractor

class TXTExtractor(DataExtractor):
    def extract(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

