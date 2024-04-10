import io

import pandas as pd
from datetime import datetime

class TXTExtractor:
    def extract(self, text_file='x.txt'):
        text_data = text_file.decode('utf-8')


        lines = [line for line in text_data.strip().split("\n") if line.strip()]
        if len(lines) < 2:
            raise ValueError("Text data does not contain sufficient information")

        # Extract the date and location
        date_string, location = lines[0].strip(), lines[1].strip()


        # Parse the date string into a datetime object
        date = datetime.strptime(date_string, '%A %d %B %Y').strftime('%d/%m/%Y').replace("\\", "")

        participants = []
        # Parse participant lines, removing carriage returns and other unwanted characters
        for line in lines[2:]:
            line = line.replace('\r', '')  # Remove carriage returns
            name, scores = line.split(" -  ")
            psychometrics, presentation = scores.split(", ")
            psychometrics_score = psychometrics.split(": ")[1]
            presentation_score = presentation.split(": ")[1].strip()  # Ensure to strip again if needed
            participants.append({
                "name": name,
                "Psychometrics": psychometrics_score,
                "Presentation": presentation_score
            })

        # Create a DataFrame
        df = pd.DataFrame(participants)
        df["Date"] = date
        df['Location'] = location

        # Convert DataFrame to JSON

        txt_JSON = df.to_json(orient='records',date_format='iso')
        tct_JSON = txt_JSON.replace('\/', '/')
        return txt_JSON
