class JSONConfigStrategy(ConfigStrategy):
    """Strategy for reading JSON configuration files."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_config(self) -> dict:
        with open(self.file_path, 'r') as file:
            return json.load(file)