import pandas as pd
import re
import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from table_extractor.column_extractor import ColumnExtractor
from table_extractor.table_row_column_index_extractor import TableRowColumnExtractor

class AlphaNumericalColumnsTableExtractor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def is_alphanumeric_or_nan(self, value):
        if pd.isna(value):
            return True  # NaN values are allowed
        if isinstance(value, str):
            stripped_value = value.strip()
            return re.match(r'^[a-zA-Z0-9_-]+$', stripped_value) is not None
        if isinstance(value, int):
            return True  # Allow numeric values
        return False

    def extract_alphanumerical_columns(self):
        alphanumeric_columns = []
        for col in self.dataframe.columns:
            all_values_alphanumeric_or_nan = True
            for value in self.dataframe[col]:
                result = self.is_alphanumeric_or_nan(value)
                if not result:
                    all_values_alphanumeric_or_nan = False
                    break
            if all_values_alphanumeric_or_nan:
                alphanumeric_columns.append(col)

        return alphanumeric_columns
    
if __name__ == "__main__":
    api_key = 'api-key'
    if len(sys.argv) != 2:
        print("Usage: python table_row_column_index_extractor.py <path_to_excel_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    column_extractor = ColumnExtractor(api_key)
    columns = column_extractor.process_file(file_path)

    df = pd.read_excel(file_path)

    extractor = TableRowColumnExtractor()
    filtered_df = extractor.construct_filtered_df(df, columns)
    column_extractor = AlphaNumericalColumnsTableExtractor(filtered_df)
    alphanumerical_columns = column_extractor.extract_alphanumerical_columns()
    print("alphanumerical columns are:")
    print(alphanumerical_columns)