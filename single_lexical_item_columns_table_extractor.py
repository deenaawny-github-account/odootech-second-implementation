import pandas as pd
import re
import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from table_extractor.column_extractor import ColumnExtractor
from table_extractor.table_row_column_index_extractor import TableRowColumnExtractor

class SingleLexicalItemColumnsTableExtractor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def is_single_lexical_item_or_nan(self, value):
        if pd.isna(value):
            return True  # NaN values are allowed
        if isinstance(value, str):
            stripped_value = value.strip()
            # A single lexical item contains only letters and numbers
            return re.match(r'^[a-zA-Z0-9_-]+$', stripped_value) is not None
        if isinstance(value, int):
            return True
        if isinstance(value, float):
            return True
        return False

    def extract_single_lexical_item_columns(self):
        single_lexical_item_columns = []
        for col in self.dataframe.columns:
            all_values_single_lexical_item_or_nan = True
            for value in self.dataframe[col]:
                result = self.is_single_lexical_item_or_nan(value)
                if not result:
                    all_values_single_lexical_item_or_nan = False
                    break
            if all_values_single_lexical_item_or_nan:
                single_lexical_item_columns.append(col)

        return single_lexical_item_columns
    
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
    print("the filtered df")
    print(filtered_df)
    column_extractor = SingleLexicalItemColumnsTableExtractor(filtered_df)
    single_lexical_item_columns = column_extractor.extract_single_lexical_item_columns()
    print("Single lexical item columns are:")
    print(single_lexical_item_columns)
