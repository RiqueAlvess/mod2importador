from typing import List
from pathlib import Path
import pandas as pd

class FileService:
    def get_file_columns(self, file_path: str, header_row: int = 0) -> List[str]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(str(file_path))
        if path.suffix.lower() in {'.csv', '.txt'}:
            df = pd.read_csv(path, header=header_row)
        else:
            df = pd.read_excel(path, header=header_row, engine='openpyxl')
        return df.columns.astype(str).tolist()
