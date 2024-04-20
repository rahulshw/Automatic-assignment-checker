from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Replace these values with your own
from secrets import *

COURSE_ID = '650653755378'
ASSIGNMENT_ID = '647076078312'
USER_ID = 'me'  # User ID you want to get the email for

# Initialize credentials
credentials = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Build the People service
service = build('people', 'v1', credentials=credentials)

def get_contacts(user_id):
    try:
        # Call the people.connections().list method to retrieve the user's contacts
        connections = service.people().connections().list(
            resourceName=f"people/{user_id}",
            pageSize=100,
            personFields='names,emailAddresses'
        ).execute()
        contacts = connections.get('connections', [])
        return contacts
    except Exception as e:
        print(f"Error retrieving contacts for user {user_id}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    user_contacts = get_contacts(USER_ID)
    if user_contacts:
        print(f"Contacts for user {USER_ID}:")
        for contact in user_contacts:
            names = contact.get('names', [])
            if names:
                name = names[0].get('displayName', 'Unknown')
            else:
                name = 'Unknown'
            email_addresses = contact.get('emailAddresses', [])
            if email_addresses:
                email = email_addresses[0].get('value', 'Unknown')
            else:
                email = 'Unknown'
            print(f"Name: {name}, Email: {email}")
    else:
        print(f"Failed to retrieve contacts for user {USER_ID}")