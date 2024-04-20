from google_auth_oauthlib.flow import InstalledAppFlow

#secrets
from secrets import *


SCOPES = [
    #'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    #'https://www.googleapis.com/auth/classroom.announcements',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.profile.emails',
    'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
    'https://www.googleapis.com/auth/contacts.readonly',
    'https://www.googleapis.com/auth/directory.readonly',
    'https://www.googleapis.com/auth/classroom.profile.emails',
    'https://www.googleapis.com/auth/classroom.rosters.readonly'

    # Add other necessary scopes here
]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret_337591355086-f3nuecbb4gvnjole6jko84b6hulfg8e4.apps.googleusercontent.com.json",
    scopes=SCOPES
)
credentials = flow.run_local_server(port=0)

print("Refresh Token:", credentials.refresh_token)