import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from empty_columns_table_extractor import AllNaNColumnsTableExtractor
from table_extractor.column_extractor import ColumnExtractor
from table_extractor.table_row_column_index_extractor import TableRowColumnExtractor

class BooleanColumnsTableExtractor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def is_boolean(self, value):
        if pd.isna(value):
            return False  # or True depending on whether you want to consider NA as boolean
        if isinstance(value, bool):
            return True
        elif isinstance(value, str) and value.lower() in ["true", "false"]:
            return True
        else:
            return False

    def convert_to_boolean(self, df):
        for column in df.columns:
            if set(df[column].dropna().unique()) <= {0.0, 1.0}:
                df[column] = df[column].astype(bool)
        return df

    def extract_boolean_columns(self):
        boolean_columns = []

        # Use AllNaNColumnsTableExtractor to filter out all-NaN columns
        nan_column_extractor = AllNaNColumnsTableExtractor(self.dataframe)
        all_nan_columns = nan_column_extractor.extract_all_nan_columns()
        filtered_df = self.dataframe.drop(columns=all_nan_columns)

        for col in filtered_df.columns:
            all_values_boolean = True
            for value in filtered_df[col]:
                if not self.is_boolean(value):
                    all_values_boolean = False
                    break
            if all_values_boolean:
                boolean_columns.append(col)
        return boolean_columns


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python boolean_columns_extractor.py <path_to_excel_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    # Assuming ColumnExtractor requires an API key
    api_key = 'api-key'
    column_extractor = ColumnExtractor(api_key)
    columns = column_extractor.process_file(file_path)

    df = pd.read_excel(file_path)
    df = df.convert_dtypes()  # Ensure appropriate dtypes

    extractor = TableRowColumnExtractor()
    filtered_df = extractor.construct_filtered_df(df, columns)

    boolean_column_extractor = BooleanColumnsTableExtractor(filtered_df)
    boolean_column_extractor.dataframe = boolean_column_extractor.convert_to_boolean(filtered_df)
    boolean_columns = boolean_column_extractor.extract_boolean_columns()
    
    print("Boolean columns are:")
    print(boolean_columns)
