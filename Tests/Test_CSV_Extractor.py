import unittest
from io import StringIO

from Classes.CSV_extractor import CSVExtractor

class TestCSVExtractor(unittest.TestCase):
    def test_extract(self):
        # Test logic for CSV extraction
        csv_data = StringIO("""id,name,gender,dob,email,city,address,postcode,phone_number,uni,degree,invited_date,month,invited_by
1,Esme Trusslove,Female,04/08/1994,etrusslove0@google.es,Swindon,22056 Lerdahl Avenue,SN1,+44 7000 000000,Saint George's Hospital Medical School, University of London,02:01,10,January 2019,Bruno Bellbrook
2,Matthaeus Audas,Male,,maudas1@mapquest.com,Charlton,263 Nelson Trail,OX12,+44 7000 000001,Keele University,02:01,30,January 2019,Doris Bellasis
3,Cherey Tollfree,Female,08/12/1992,ctollfree2@netvibes.com,Weston,69 Coleman Court,GU32,+44 7000 000002,King's College London, University of London,02:01,25,January 2019,Gismo Tilling
""")


        # Use the CSVExtractor to read the sample data
        extractor = CSVExtractor()
        df = extractor.extract(csv_data)

        # Perform some assertions
        self.assertEqual(len(df), 3)  # Expecting 3 rows of data
        self.assertTrue('name' in df.columns)  # 'id' column should exist
        self.assertTrue(df['phone_number'].str.startswith('+44').all())  # All phone numbers should start with +44

        # Check the replacement of empty month values
        self.assertFalse(df['month'].isna().any())  # No NaN values expected in 'month' column
        self.assertTrue((df['month'] == 'January 2019').any())  # At least one entry with 'January 2019'

