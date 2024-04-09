import pandas as pd
from Datetime import Datetime

class TXTExtractor:
    def extract(self, text_file):
        with open(text_file, 'r') as file:
            text_data = file.read()
        lines = [line for line in text_data.strip().split("\n") if line.strip()]
        if len(lines) < 2:
            raise ValueError("Text data does not contain sufficient information")

        # Extract the date and location
        date, location = lines[0], lines[1]

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
        return txt_JSON

