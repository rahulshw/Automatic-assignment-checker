from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Replace these values with your own
from secrets import *

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

# Function to get all assignments for a specific course
def get_assignments(course_id):
    results = service.courses().courseWork().list(
        courseId=course_id
    ).execute()

    assignments = results.get('courseWork', [])

    return assignments

# Example usage
course_id = '650653755378'
assignments = get_assignments(course_id)

from pprint import pprint
pprint(assignments)
# Print assignment details
# for assignment in assignments:
#     print(f"Assignment: {assignment['title']}")
#     print(f"ID: {assignment['id']}")
#     print(f"Description: {assignment.get('description', 'No description')}")
#     print(f"Due Date: {assignment.get('dueDate', 'No due date')}")
#     print(assignment)
