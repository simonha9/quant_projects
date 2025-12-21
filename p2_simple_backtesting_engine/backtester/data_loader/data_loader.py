# Data Loader class
from pathlib import Path
import pandas as pd

class DataLoaderError(Exception):
    """Raised when DataLoader encounters an error."""
    pass

class DataLoader:

    filepath = None

    def __init__(self, filepath: str):
        path = Path(filepath)
        # let's do some filepath validation
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        if path.suffix.lower() != ".csv":
            raise ValueError(f"Expected a .csv file, got: {path.suffix}")

        if path.stat().st_size == 0:
            raise ValueError(f"CSV file is empty: {path}")

        # Actually try to read it
        try:
            with path.open("r", encoding="utf-8") as f:
                f.readline()
        except Exception as e:
            raise ValueError(f"CSV file is not readable: {path}") from e


        self.filepath = filepath

    def read_data(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.filepath)
            return df
        except Exception as e:
            raise DataLoaderError("Failed to read CSV") from e