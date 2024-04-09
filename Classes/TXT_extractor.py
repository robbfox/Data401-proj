import pandas as pd
from datetime import datetime

class TXTExtractor:
    def extract(self, text_file='x.txt'):
        with open(text_file, 'r') as file:
            text_data = file.read()
        lines = [line for line in text_data.strip().split("\n") if line.strip()]
        if len(lines) < 2:
            raise ValueError("Text data does not contain sufficient information")

        # Extract the date and location
        date_string, location = lines[0], lines[1]

        # Parse the date string into a datetime object
        date = datetime.strptime(date_string, '%A %d %B %Y').strftime('%d/%m/%Y')

        participants = []
        # Parse participant lines
        for line in lines[2:]:
            name, scores = line.split(" -  ")
            psychometrics, presentation = scores.split(", ")
            psychometrics_score = psychometrics.split(": ")[1]
            presentation_score = presentation.split(": ")[1]
            participants.append(
                {"name": name, "Psychometrics": psychometrics_score, "Presentation": presentation_score})

        # Create a DataFrame
        df = pd.DataFrame(participants)
        df["Date"] = date
        df['Location'] = location
        txt_JSON = df.to_json(orient='records')
        print(txt_JSON)
