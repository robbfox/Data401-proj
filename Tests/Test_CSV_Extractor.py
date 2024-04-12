import unittest
from io import StringIO
from datetime import datetime

from Classes.CSV_extractor import CSVExtractor

class TestCSVExtractor(unittest.TestCase):




    def test_extract(self):
        # Test logic for CSV extraction
        csv_data = StringIO("""id,name,gender,dob,email,city,address,postcode,phone_number,uni,degree,invited_date,month,invited_by
1,Vachel Mc Meekin,Male,13/02/2000,vmc0@businesswire.com,Upton,8 Swallow Point,WF9,+44 (594) 165-3629,Thames Valley University,02:02,28,Feb-19,Bruno Bellbrook
2,Wilfrid Warde,Male,25/05/1992,wwarde1@cbstocal.com,Newtown,2626 Lawn Pass,RG20,44-638-479-6556,University of Central Lancashire,02:02,12,Feb-19,Gismo Tilling
3,Cameron Gleaves,Male,29/05/2000,cgleaves2@gizmodo.com,Weston,937th Crossing,GU32,44-522-751-6028,Cardiff University,1st,13,Feb-19,Bruno Bellbrook
4,Felicio Betjeman,Male,02/11/1996,fbetjeman3@etsy.com,Sheffield,33584 Crescent Oaks Park,S33,+44 (249) 276-2047,Thames Valley University,02:01,14,Feb-19,Gismo Tilling
5,Hakeem Ivermee,Male,04/05/1994,hivermee4@yale.edu,Whitchurch,46413 Lunder Alley,BS14,+44 387 443 3095,University of Salford,02:01,19,Feb-19,Sunny Sladefield
6,Ian Giorgietto,Male,,igiorgietto5@cmu.edu,Sheffield,3 Corscot Place,S33,+44 786 239 9666,,3rd,28,Feb-19,Stacey Broad
        """)
        csv_encoded = csv_data.getvalue().encode('utf-8')

        # Use the CSVExtractor to read the sample data
        extractor = CSVExtractor()
        df = extractor.extract(csv_encoded,"feb2019Applications.csv")
        def is_valid_date(date_str):
            try:
                if date_str:
                    datetime.strptime(date_str, '%d/%m/%Y')  # parse date
                return True
            except ValueError:
                return False
        self.assertEqual(len(df), 6)
        self.assertTrue('name' in df.columns)
        self.assertTrue(df['phone_number'].str.startswith('+44').all())  # All phone numbers should start with +44
        self.assertTrue(all(df['Date'].apply(is_valid_date)), "One or more dates are in the incorrect format.")


