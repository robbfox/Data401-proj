##from data_extractor import DataExtractor
import pandas as pd
import numpy as np


class CSVExtractor:
    @staticmethod
    def extract(file_path):
        # Read CSV file
        df = pd.read_csv(file_path)

        # Change all empty "month" category to "January 2019"
        df.loc[pd.isna(df['month']), 'month'] = 'January 2019'

        # Change all empty cells in each category (except 'month') to NaN
        df.replace('', np.nan, inplace=True)

        # Function to standardize phone numbers
        def standardize_phone(phone):
            # Check if phone number is NaN
            if pd.isna(phone):
                return np.nan

            # Remove non-digit characters
            digits_only = ''.join(filter(str.isdigit, phone))

            # Format phone number uniformly
            formatted_phone = '+44 {} {} {}'.format(digits_only[2:5], digits_only[5:8], digits_only[8:])

            return formatted_phone

        # Apply the standardize_phone function to each phone number
        df['phone_number'] = df['phone_number'].apply(standardize_phone)

        return df

