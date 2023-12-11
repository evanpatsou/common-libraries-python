class CSVConfigStrategy(ConfigStrategy):
    """Strategy for reading CSV configuration files."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_config(self) -> list:
        with open(self.file_path, mode='r') as file:
            return list(csv.DictReader(file))