import openai
import pandas as pd
import os
import json

class ColumnExtractor:
    def __init__(self, api_key):
        openai.api_key = api_key

    def read_text_from_file(self, file_path):
        """
        Reads text from CSV or Excel files.
        """
        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == '.csv':
            df = pd.read_csv(file_path)
            text = df.to_string(index=False)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
            text = df.to_string(index=False)
        else:
            raise ValueError("Unsupported file format. Supported formats: CSV, Excel.")
        
        return text, df

    def extract_column_names_with_llm(self, df):
        """
        Uses LLM to identify and extract column names.
        """
        data_summary = df.head(20).to_string(index=False)
        prompt_template = """
        The following is a table of product data. 

        {data_summary}

        Provide the standardized table with only the column names. Delete all data, surrounding logos and empty cells.            
        """
        
        prompt = prompt_template.format(data_summary=data_summary)

        functions = [
            {
                "name": "get_column_names",
                "description": "Extract column names from the provided data preview.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "columns": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                },
                "required": ["columns"]
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            functions=functions,
            function_call="auto"
        )

        # Extract and format the response as a JSON object
        json_response = json.loads(response.choices[0].message['function_call']['arguments'])
        return json_response['columns']

    def process_file(self, file_path):
        text, df = self.read_text_from_file(file_path)
        columns = self.extract_column_names_with_llm(df)
        return columns

if __name__ == "__main__":
    api_key = 'api-key'
    file_path = input("Enter the file path of the Excel sheet: ")

    column_extractor = ColumnExtractor(api_key)
    columns = column_extractor.process_file(file_path)
    print("the columns are")
    print(columns)
