import pandas as pd
import re
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from table_extractor.column_extractor import ColumnExtractor
from table_extractor.table_row_column_index_extractor import TableRowColumnExtractor

class AllFloatColumnsTableExtractor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def is_float(self, value):
        if pd.isna(value):
            return True  # Allow NaN values in float columns
        return isinstance(value, float)

    def extract_all_float_columns(self):
        all_float_columns = []
        for col in self.dataframe.columns:
            all_values_float = True
            for value in self.dataframe[col]:
                result = self.is_float(value)
                if not result:
                    all_values_float = False
                    break
            if all_values_float:
                all_float_columns.append(col)
        return all_float_columns

if __name__ == "__main__":
    api_key = 'api-key'
    if len(sys.argv) != 2:
        print("Usage: python all_float_columns_extractor.py <path_to_excel_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    column_extractor = ColumnExtractor(api_key)
    columns = column_extractor.process_file(file_path)

    df = pd.read_excel(file_path)

    extractor = TableRowColumnExtractor()
    filtered_df = extractor.construct_filtered_df(df, columns)
    float_column_extractor = AllFloatColumnsTableExtractor(filtered_df)
    all_float_columns = float_column_extractor.extract_all_float_columns()
    print("All-float columns are:")
    print(all_float_columns)
