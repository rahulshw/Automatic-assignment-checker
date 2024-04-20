from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

# Replace these values with your own
from secrets import *

COURSE_ID = '650653755378'

# Initialize credentials
credentials = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Build the Classroom service
service = build('classroom', 'v1', credentials=credentials)

def list_students(course_id):
    students_dict = {}
    page_token = None
    
    while True:
        response = service.courses().students().list(
            courseId=course_id,
            pageSize=100,  # Adjust as needed
            pageToken=page_token
        ).execute()
        students = response.get('students', [])
        for student in students:
            user_id = student['userId']
            students_dict[user_id] = dict(roll_number = student['profile']['name']['familyName'], name=student['profile']['name']['givenName'], asg1_marks=0)
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    
    return students_dict

# Example usage
if __name__ == "__main__":
    students = list_students(COURSE_ID)
    with open('students_asg_2.json', 'w') as fp:
        json.dump(students, fp)