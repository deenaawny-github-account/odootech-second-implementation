import sys
import os
import pandas as pd

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from table_extractor.column_extractor import ColumnExtractor

class TableRowColumnExtractor:
    def __init__(self):
        pass

    def extract_row_values(self, df):
        row_values_list = []

        def get_row_values(row):
            row_values = list(row)
            row_values_list.append(row_values)
        
        # Iterating over rows using apply()
        df.apply(get_row_values, axis=1)
    
        return row_values_list
    
    def extract_row_indices_with_values(self, df, target_values):
        print("extract row indices with values")
        print(target_values)
        matching_indices = []

        def check_row(row):
            row_values = list(row)
            if all(val in row_values for val in target_values):
                matching_indices.append(row.name)

        # Iterating over rows using apply()
        df.apply(check_row, axis=1)
    
        return matching_indices
    
    def construct_filtered_df(self, df, target_values):
        matching_indices = self.extract_row_indices_with_values(df, target_values)
        print("matching indicies")
        print(matching_indices)
        if matching_indices:
            first_matching_index = matching_indices[0]
            filtered_df = df.loc[first_matching_index+1:].reset_index(drop=True)
            filtered_df.columns = df.iloc[first_matching_index]  # Set headers to the matching row
            filtered_df.columns.name = None  # Ensure the headers index is null
        else:
            filtered_df = df  # No matching rows, return the same DataFrame
        
        return filtered_df
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python table_row_column_index_extractor.py <path_to_excel_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    api_key = 'api-key'
    column_extractor = ColumnExtractor(api_key)
    columns = column_extractor.process_file(file_path)

    df = pd.read_excel(file_path)

    extractor = TableRowColumnExtractor()
    filtered_df = extractor.construct_filtered_df(df, columns)

    print(f"The filtered DataFrame for {file_path}:")
    print(filtered_df)
