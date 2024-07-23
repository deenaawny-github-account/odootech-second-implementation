import pandas as pd

class ExcelProcessor:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.columns_to_keep = []

    def set_columns_to_keep(self, columns):
        self.columns_to_keep = [col.strip().lower() for col in columns]

    def remove_empty_rows(self, df, column):
        column = column.strip().lower()  # Normalize the column name
        return df.dropna(subset=[column])

    def remove_rows_with_value(self, df, value):
        return df[~df.isin([value]).any(axis=1)]

    def replace_value(self, df, value, replacement=''):
        return df.replace(value, replacement)

    def filter_columns(self, first_data_row, first_data_col):
        try:
            # Load the Excel file without header
            df = pd.read_excel(self.input_file_path, header=None)

            # Slice the DataFrame to remove text or logos
            df = df.iloc[first_data_row:, first_data_col:]
            df.columns = df.iloc[0].str.strip().str.lower()  # Strip trailing whitespaces and convert to lowercase
            df = df.drop(df.index[0]).reset_index(drop=True)
            
            # Check if the columns are set
            if not self.columns_to_keep:
                raise ValueError("No columns specified to keep. Please set the columns using set_columns_to_keep method.")
            
            # Keep only the specified columns
            filtered_df = df[self.columns_to_keep].copy()  # Explicitly create a copy

            # Rename the columns to standard names
            filtered_df.columns = ["product item code", "quantity", "product price"]

            # Save the filtered DataFrame back to a new Excel file
            filtered_df.to_excel(self.output_file_path, index=False)

            print("Filtered file saved successfully!")
        except KeyError as e:
            print(f"Error: {e}. Please check the column names and try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def process_file(self, first_data_row, first_data_col):
        self.filter_columns(first_data_row, first_data_col)
        return pd.read_excel(self.output_file_path)

    def process_hid_pricelist(self, first_data_row, first_data_col):
        df_filtered = self.process_file(first_data_row, first_data_col)
        df_filtered = self.remove_empty_rows(df_filtered, 'quantity')
        df_filtered = self.replace_value(df_filtered, 'OID', '')
        df_filtered = self.replace_value(df_filtered, 'VIZ', '')
        df_filtered = df_filtered.drop(df_filtered.index[0])
        list_of_lists = df_filtered.values.tolist()
        grouped_products = group_products(list_of_lists)
        result = []
        for group in grouped_products:
            result.append(repeat_products(group))
        flattened_list = flatten_list(result)
        df = pd.DataFrame(flattened_list, columns=['product item code', 'quantity', 'product price'])
        df = self.remove_empty_rows(df, 'product item code')
        return self.replace_quantity_values(df)

    def replace_quantity_values(self, df):
        replacements = {
            'MOQ-5k': '5000',
            'MOQ-2k': '2000',
            '2k-5k': '5000',
            '2.5k-5k': '5000',
            '1k-2.5k': '2500',
            '5k-10k': '10000',
            '10k-20k': '20000',
            '20k-50k': '50000',
            '50k-100k': '100000',
            'MOQ-1k': '10000'
        }
        for old_value, new_value in replacements.items():
            df = self.replace_value(df, old_value, new_value)
        return df

def transform_table(df):
    transformed_rows = []
    current_product_name = None
    for index, row in df.iterrows():
        if pd.notna(row[0]):  
            current_product_name = row[0]
        transformed_rows.append([current_product_name, row[1], row[2]])
    transformed_df = pd.DataFrame(transformed_rows, columns=['product item code', 'quantity', 'product price'])
    return transformed_df

def group_products(data):
    grouped = []
    current_group = []
    for entry in data:
        if entry[1] == 'MOQ-5k': 
            if current_group: 
                grouped.append(current_group)
            current_group = [entry]
        else:
            current_group.append(entry)
    if current_group:  
        grouped.append(current_group)
    return grouped

def repeat_products(data):
    result = []
    product_names = [row[0] for row in data if row[0] != '']
    for product_name in product_names:
        for row in data:
            result.append([product_name, row[1], row[2]])
    return result

def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]

def find_new_products(df1, df2, product_column='product item code'):
    df1_products = set(df1[product_column])
    df2_products = set(df2[product_column])
    new_products = list(df2_products - df1_products)
    return new_products

def find_obsolete_products(df1, df2, product_column='product item code'):
    df1_products = set(df1[product_column])
    df2_products = set(df2[product_column])
    obsolete_products = list(df1_products - df2_products)
    return obsolete_products

def find_changed_price_products(df1, df2, price_column='product price', product_column='product item code', quantity_column='quantity'):
    # Ensure both quantity columns are of the same type
    df1[quantity_column] = df1[quantity_column].astype(str)
    df2[quantity_column] = df2[quantity_column].astype(str)
    
    merged_df = pd.merge(df1, df2, on=[product_column, quantity_column], suffixes=('_df1', '_df2'))
    print("the merged df")
    print(merged_df)
    changed_price_products = merged_df[merged_df[f'{price_column}_df1'] != merged_df[f'{price_column}_df2']]
    return changed_price_products[[product_column, quantity_column]]

if __name__ == "__main__":
    # Process product_template.xlsx
    processor = ExcelProcessor('sample_files/product_template.xlsx', 'sample_files/filtered_product_template.xlsx')
    processor.set_columns_to_keep(['seller_ids/product_code', 'seller_ids/min_qty', 'seller_ids/price'])
    df_product_template = processor.process_file(0, 0)

    # Process hid_pricelist.xlsx
    processor = ExcelProcessor('sample_files/hid_pricelist.xlsx', 'sample_files/filtered_hid_pricelist.xlsx')
    processor.set_columns_to_keep(['part no.', 'quantity break', 'app'])
    df_hid_pricelist = processor.process_hid_pricelist(2, 0)
    df_hid_pricelist.to_excel('sample_files/filtered_hid_pricelist_temp.xlsx', index=False)

    # Find new and obsolete products
    new_products = find_new_products(df_product_template, df_hid_pricelist)
    obsolete_products = find_obsolete_products(df_product_template, df_hid_pricelist)

    # Find changed price products
    changed_price_products = find_changed_price_products(df_product_template, df_hid_pricelist)

    print("New Products:", new_products)
    print("Obsolete Products:", obsolete_products)
    ##print("Changed Price Products:")
    print(changed_price_products)