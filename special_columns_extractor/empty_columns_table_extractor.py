import pandas as pd
import re
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from table_extractor.column_extractor import ColumnExtractor
from table_extractor.table_row_column_index_extractor import TableRowColumnExtractor

class AllNaNColumnsTableExtractor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def is_nan(self, value):
        return pd.isna(value)

    def extract_all_nan_columns(self):
        all_nan_columns = []
        for col in self.dataframe.columns:
            all_values_nan = True
            for value in self.dataframe[col]:
                result = self.is_nan(value)
                if not result:
                    all_values_nan = False
                    break
            if all_values_nan:
                all_nan_columns.append(col)
        return all_nan_columns

if __name__ == "__main__":
    api_key = 'api-key'
    if len(sys.argv) != 2:
        print("Usage: python all_nan_columns_extractor.py <path_to_excel_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    column_extractor = ColumnExtractor(api_key)
    columns = column_extractor.process_file(file_path)

    df = pd.read_excel(file_path)

    extractor = TableRowColumnExtractor()
    filtered_df = extractor.construct_filtered_df(df, columns)
    nan_column_extractor = AllNaNColumnsTableExtractor(filtered_df)
    all_nan_columns = nan_column_extractor.extract_all_nan_columns()
    print("All-NaN columns are:")
    print(all_nan_columns)
