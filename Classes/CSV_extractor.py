##from data_extractor import DataExtractor
import io

import pandas as pd
import numpy as np

## TO GET ALL COLUMNS
pd.set_option('display.max_rows', 500)  # or use None to display all rows
pd.set_option('display.max_columns', None)  # Display all columns


class CSVExtractor:


    @staticmethod
    def extract(file_path):
        # Function to standardize phone numbers
        def standardize_phone(phone):
            # Check if phone number is NaN
            if pd.isna(phone):
                return np.nan

            # Remove non-digit characters
            digits_only = ''.join(filter(str.isdigit, phone))

            # Ensure there are enough digits for formatting
            if len(digits_only) >= 10:
                # Format phone number uniformly, assuming UK country code (+44) and standard length
                formatted_phone = '+44 {} {} {}'.format(digits_only[-10:-7], digits_only[-7:-4], digits_only[-4:])
                return formatted_phone
            else:
                # Return the original phone number if it doesn't meet criteria
                return phone

        # Convert bytes object to file-like object and read CSV file
        df = pd.read_csv(io.BytesIO(file_path))

        # Check the condition based on the number of columns
        if len(df.columns) == 50:
            # Apply fillna(0) in-place
            df.fillna(0, inplace=True)
        else:
            # Change all empty "month" category to "January 2019"
            df.loc[pd.isna(df['month']), 'month'] = 'January 2019'

            # Change all empty cells in each category (except 'month') to NaN
            df.replace('', np.nan, inplace=True)

            # Apply the standardize_phone function to each phone number correctly
            df['phone_number'] = df['phone_number'].apply(standardize_phone)

        return df



