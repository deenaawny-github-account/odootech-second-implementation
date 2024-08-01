import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from special_columns_extractor.boolean_columns_table_extractor import BooleanColumnsTableExtractor
from special_columns_extractor.empty_columns_table_extractor import AllNaNColumnsTableExtractor
from table_extractor.column_extractor import ColumnExtractor
from table_extractor.table_row_column_index_extractor import TableRowColumnExtractor

class CurrencyColumnsTableExtractor:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def filter_all_nan_rows(self):
        self.dataframe = self.dataframe.dropna(how='all')
        
    def filter_all_nan_columns(self):
        # Use AllNaNColumnsTableExtractor to filter out all-NaN columns
        nan_column_extractor = AllNaNColumnsTableExtractor(self.dataframe)
        all_nan_columns = nan_column_extractor.extract_all_nan_columns()
        self.dataframe = self.dataframe.drop(columns=all_nan_columns)
        self.dataframe = self.dataframe.convert_dtypes()  # Ensure appropriate dtypes

    def detect_currency_columns(self, currencies=['USD', 'EGP']):
        currency_columns = []
        for column in self.dataframe.columns:
            if self.dataframe[column].dtype == 'object':
                if self.dataframe[column].apply(lambda x: any(currency in str(x) for currency in currencies)).any():
                    currency_columns.append(column)
        return currency_columns

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
    
    extractor = TableRowColumnExtractor()
    filtered_df = extractor.construct_filtered_df(df, columns)

    currency_column_extractor = CurrencyColumnsTableExtractor(filtered_df)
    currency_columns = currency_column_extractor.detect_currency_columns()
    
    print("Currency columns are:")
    print(currency_columns)
