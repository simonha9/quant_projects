import pytest
import tempfile
import os
import pandas as pd
from pathlib import Path
from backtester.data_loader.data_loader import DataLoader

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        DataLoader("nonexistent.csv")

def test_wrong_extension():
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        with pytest.raises(ValueError, match="Expected a .csv file"):
            DataLoader(tmp.name)

def test_empty_file():
    with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
        # ensure file is empty
        tmp.truncate(0)
        tmp.flush()
        with pytest.raises(ValueError, match="CSV file is empty"):
            DataLoader(tmp.name)

def test_valid_csv():
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=False) as tmp:
        tmp.write("col1,col2\n1,2\n")
        tmp.flush()
        tmp_path = tmp.name

    
    try:
        # initialize DataLoader
        loader = DataLoader(tmp_path)
        
        # read data
        df = loader.read_data()
        
        # assertions
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert list(df.columns) == ["col1", "col2"]
        assert df.iloc[0]["col1"] == 1
        assert df.iloc[0]["col2"] == 2

    finally:
        # cleanup temporary file
        os.remove(tmp_path)
