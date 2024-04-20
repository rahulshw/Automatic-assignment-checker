import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PyPDF2 import PdfReader
import json

# Replace these values with your own
from secrets import *

COURSE_ID = '650653755378'
ASSIGNMENT_ID = '647450938601' #'647076078312'
MARKS_FILENAME = 'students.json'

# Initialize credentials
credentials = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Build the Classroom service
service_classroom = build('classroom', 'v1', credentials=credentials)

# Build the Drive service
service_drive = build('drive', 'v3', credentials=credentials)
with open(MARKS_FILENAME, 'r') as fp:
    student_data = json.load(fp)

# Function to download PDF submission
def download_submission(submission_id, file_id, user_id):
    try:
        request = service_drive.files().get_media(fileId=file_id)
        with open(os.path.join('submissions', f"{user_id}.pdf"), 'wb') as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        return True
    except Exception as e:
        print(f"Error downloading submission for user {user_id}: {e}")
        return False


# Function to grade submissions
def grade_submissions(submissions, counter):
    for submission in submissions:
        try:
            submission_id = submission['id']
            user_id = submission.get('userId', 'Unknown')
            attachments = submission.get('assignmentSubmission', {}).get('attachments', [])
            if not attachments:
                # No attachments, assignment not submitted
                grade_submission(user_id, 0)
                continue
            attachment = attachments[0]
            file_id = attachment.get('driveFile', {}).get('id')
            if not file_id:
                # Attachment is not a Google Drive file
                grade_submission(user_id, 0)
                continue

            if download_submission(submission_id, file_id, user_id):
                # Check if file download was successful
                if os.path.isfile(os.path.join('submissions', f"{user_id}.pdf")):
                    # Check number of pages in the PDF
                    with open(os.path.join('submissions', f"{user_id}.pdf"), 'rb') as file:
                        pdf_reader = PdfReader(file)
                        num_pages = len(pdf_reader.pages)
                        if num_pages == 0:
                            # Grade the submission 0 if not submitted
                            grade_submission(user_id, 0)
                        elif num_pages == 1:
                            # Grade the submission 5 if 1 page
                            grade_submission(user_id, 8)
                        else:
                            # Grade the submission 10 if more than 1 page
                            grade_submission(user_id, 10)
                else:
                    print(f"Error downloading PDF file for user {user_id}")
            else:
                # Assignment not submitted or error downloading file
                grade_submission(user_id, 0)

        except Exception as e:
            print(f"Error processing submission for user {user_id}: {e}")
            # Save the index of the last processed submission
            save_last_processed_index(submissions.index(submission))
        
        counter = counter+1
        print(f'submitted count: {counter}')

def save_students_data():
    with open(MARKS_FILENAME, 'w') as fp:
        json.dump(student_data, fp)

# Function to grade a submission
def grade_submission(user_id, grade):
    student_data[user_id]['asg2_marks'] = grade
    print(f'user_id: {user_id}, marks: {grade}')
    

# Function to save the index of the last processed submission
def save_last_processed_index(index):
    with open('last_processed_index.json', 'w') as file:
        json.dump(index, file)
    save_students_data()
    

# Function to load the index of the last processed submission
def load_last_processed_index():
    if os.path.exists('last_processed_index.json'):
        with open('last_processed_index.json', 'r') as file:
            return json.load(file)
    else:
        return None

# Function to save processed submission IDs
def save_processed_submissions(submission_ids):
    with open('processed_submissions.json', 'w') as file:
        json.dump(submission_ids, file)
    save_students_data()

# Function to load processed submission IDs
def load_processed_submissions():
    if os.path.exists('processed_submissions.json'):
        with open('processed_submissions.json', 'r') as file:
            return json.load(file)
    else:
        return []

# Get all submissions for the assignment
def get_submissions(course_id, assignment_id):
    results = service_classroom.courses().courseWork().studentSubmissions().list(
        courseId=course_id,
        courseWorkId=assignment_id
    ).execute()

    submissions = results.get('studentSubmissions', [])
    return submissions

# Example usage
def main():
    last_processed_index = load_last_processed_index()
    counter = 0 if not last_processed_index else last_processed_index
    processed_submissions = load_processed_submissions()
    submissions = get_submissions(COURSE_ID, ASSIGNMENT_ID)
    submissions_to_process = [submission for submission in submissions if submission['id'] not in processed_submissions]
    if submissions_to_process:
        if last_processed_index is not None:
            submissions_to_process = submissions_to_process[last_processed_index + 1:]
        grade_submissions(submissions_to_process, counter)
        processed_submission_ids = [submission['id'] for submission in submissions_to_process]
        save_processed_submissions(processed_submission_ids)
    else:
        print("All submissions have already been processed.")

if __name__ == "__main__":
    main()