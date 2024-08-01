import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from special_columns_extractor.empty_columns_table_extractor import AllNaNColumnsTableExtractor

class ThreeToSixValueColumnsTableLabeler:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_dataframe(self):
        return self.dataframe

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def filter_all_nan_columns(self):
        nan_column_extractor = AllNaNColumnsTableExtractor(self.dataframe)
        all_nan_columns = nan_column_extractor.extract_all_nan_columns()
        self.dataframe = self.dataframe.drop(columns=all_nan_columns)
        self.dataframe = self.dataframe.convert_dtypes()  # Ensure appropriate dtypes
    
    def filter_all_nan_rows(self):
        self.dataframe = self.dataframe.dropna(how='all')

    def extract_three_to_six_value_columns(self):
        three_to_six_value_columns = []
        for col in self.dataframe.columns:
            unique_non_na_values_count = len(set(self.dataframe[col].dropna().unique()))
            if 3 <= unique_non_na_values_count <= 6:
                three_to_six_value_columns.append(col)
        return three_to_six_value_columns

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python same_value_columns_labeler.py <path_to_excel_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    df = pd.read_excel(file_path)
    
    three_to_six_value_column_labeler = ThreeToSixValueColumnsTableLabeler(df)
    three_to_six_value_column_labeler.filter_all_nan_columns()
    three_to_six_value_column_labeler.filter_all_nan_rows()
    three_to_six_value_columns = three_to_six_value_column_labeler.extract_three_to_six_value_columns()
    
    print("Three to six value columns are:")
    print(three_to_six_value_columns)
