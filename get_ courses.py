from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# secrets
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

# Function to get all courses
def get_courses():
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    return courses

# Example usage
courses = get_courses()

# Print course details
for course in courses:
    print(f"Course Name: {course['name']}")
    print(f"ID: {course['id']}")
    print(f"Description: {course.get('description', 'No description')}")
    print()
