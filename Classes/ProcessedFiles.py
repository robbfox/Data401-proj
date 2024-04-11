class ProcessedFilesManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_processed_files_list(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []

    def write_processed_file(self, file_name):
        with open(self.file_path, 'a') as file:
            file.write(file_name + '\n')