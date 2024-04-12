from pymongo import MongoClient
from datetime import datetime
from mongo_atlas_connect import *

class CandidateAnalytics:
    def __init__(self):
        self.collection = db['Candidates']  # Assuming 'Candidate' is your collection name

    def candidates_declined_offer(self):
        """
        Counts candidates who passed the interview but did not join the academy.
        """
        passed_interview = self.collection.count_documents({
            "interview_overview.result": "Pass",
            "academy_scores.Analytic_W1": {"$exists": False}
        })
        total_passed = self.collection.count_documents({
            "interview_overview.result": "Pass"
        })

        if total_passed == 0:  # Prevent division by zero
            return 0

        percentage_declined = (passed_interview / total_passed) * 100
        return percentage_declined

    def applications_by_program_and_month(self, program, year, month):
        """
        Counts applications by program for a specified month and year,
        ignoring the exact day. Dates are stored as strings in the format dd/mm/yyyy.
        """
        # Format the month to ensure it is two digits
        formatted_month = f"{month:02d}"
        # Construct a string pattern to match the month and year in the date strings
        date_pattern = f"/{formatted_month}/{year}"

        count = self.collection.count_documents({
            "interview_overview.date": {"$regex": date_pattern},
            "interview_overview.course_interest": program
        })
        return count

    def total_academy_attendees(self):
        count = self.collection.count_documents({
            "academy_scores": {"$ne": None}  # Count documents where academy_scores is not null
        })
        return count

    def total_academy_passes(self):
        pipeline = [
            {"$match": {"academy_scores": {"$ne": None}}},  # Only consider non-null academy_scores
            {"$project": {
                "scores_array": {"$objectToArray": "$academy_scores"}
            }},
            {"$match": {
                "scores_array.v": {"$ne": 0}  # No score should be 0
            }},
            {"$count": "pass_count"}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]['pass_count'] if result else 0

    def total_academy_failures(self):
        pipeline = [
            {"$match": {"academy_scores": {"$ne": None}}},  # Consider only non-null academy_scores
            {"$project": {
                "scores_array": {"$objectToArray": "$academy_scores"}
            }},
            {"$match": {
                "scores_array": {"$elemMatch": {"v": 0}}  # At least one score should be 0
            }},
            {"$count": "fail_count"}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]['fail_count'] if result else 0

    def percentage_passed(self):
        total_attendees = self.total_academy_attendees()
        total_passes = self.total_academy_passes()
        percentage = (total_passes / total_attendees * 100) if total_attendees else 0
        return percentage

    def pass_rates_by_program(self):
        pipeline = [
            # Only include documents where academy_scores is not null
            {"$match": {"academy_scores": {"$ne": None}}},

            # Project scores_array for easy checking and include course_interest
            {"$project": {
                "course_interest": "$interview_overview.course_interest",
                "scores_array": {"$objectToArray": "$academy_scores"}
            }},

            # Determine whether the candidate passed (no scores of 0)
            {"$addFields": {
                "passed": {"$not": {"$in": [0, "$scores_array.v"]}}
            }},

            # Group by course_interest to count totals and passes
            {"$group": {
                "_id": "$course_interest",
                "total_attended": {"$sum": 1},
                "total_passed": {"$sum": {"$cond": ["$passed", 1, 0]}}
            }},

            # Calculate the pass rate per program
            {"$project": {
                "program": "$_id",
                "total_attended": 1,
                "total_passed": 1,
                "percent_passed": {"$multiply": [{"$divide": ["$total_passed", "$total_attended"]}, 100]}
            }}
        ]

        # Execute the pipeline and return the results
        return list(self.collection.aggregate(pipeline))

    def top_inviters_for_passed_candidates(self):
        pipeline = [
            # Match documents where candidates passed the interview and attended the academy
            {"$match": {
                "academy_scores": {"$ne": None},
                "interview_overview.result": "Pass"
            }},
            # Group by the 'invited_by' field and count the number of such candidates
            {"$group": {
                "_id": "$personal_info.invited_by",
                "count_passed_candidates": {"$sum": 1}
            }},
            # Sort the result by the count of passed candidates in descending order
            {"$sort": {"count_passed_candidates": -1}},
            # Limit to the top 3 inviters
            {"$limit": 3}
        ]

        # Execute the pipeline
        result = list(self.collection.aggregate(pipeline))
        return result










