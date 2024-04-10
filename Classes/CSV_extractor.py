import io
from datetime import datetime
import pandas as pd
import numpy as np
import re
from dateutil.parser import parse

# To get all columns
pd.set_option('display.max_rows', None)  # or None to display all rows
pd.set_option('display.max_columns', None)  # Display all columns

class CSVExtractor:
    @staticmethod
    def extract(file_path, filename):

        # Function to standardize phone numbers
        def standardize_phone(phone):
            if pd.isna(phone):
                return np.nan
            digits_only = ''.join(filter(str.isdigit, phone))
            if len(digits_only) >= 10:
                formatted_phone = '+44 {} {} {}'.format(digits_only[-10:-7], digits_only[-7:-4], digits_only[-4:])
                return formatted_phone
            else:
                return phone

        # Convert bytes object to file-like object and read CSV file
        df = pd.read_csv(io.BytesIO(file_path))

        if len(df.columns) ==14:

            # Extract month and year from filename for the 'month' column
            stripped_filename = filename.split('/')[-1].split('.')[0]
            month_year_match = re.search(r"([a-zA-Z]+)(\d{4})", stripped_filename)
            if month_year_match:
                month_year = f"{month_year_match.group(1)} {month_year_match.group(2)}"
                try:
                    # Attempt to parse the 'month_year' string to datetime and format as 'MM/YYYY'
                    parsed_date = parse(month_year)
                    df['month'] = parsed_date.strftime('%m/%Y')
                except ValueError as e:
                    print(f"Error processing date format in filename: {filename}, Error: {e}")
                    df['month'] = np.nan  # Assign 'nan' if parsing fails

            # Ensure 'invited_date' is filled and format as two-digit day
            df['invited_date'] = df['invited_date'].fillna(1).apply(lambda x: str(int(float(x))).zfill(2))

            # Attempt to create 'Date' column by combining 'invited_date' and 'month', handling 'nan' values
            df['Date'] = df.apply(lambda row: f"{row['invited_date']}/{row['month']}" if pd.notna(row['month']) else np.nan, axis=1)
            try:
                # Convert 'Date' to datetime format only for non-nan values
                df.loc[pd.notna(df['Date']), 'Date'] = pd.to_datetime(df.loc[pd.notna(df['Date']), 'Date'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
            except ValueError as e:
                print(f"Error formatting 'Date' column: {e}")

            # Standardize phone numbers
            df['phone_number'] = df['phone_number'].apply(standardize_phone)

            return df

        else:
            df.fillna(0, inplace=True)
            return df
