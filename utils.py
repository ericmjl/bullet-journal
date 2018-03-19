from __future__ import print_function

import datetime
import os

import httplib2
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
home_dir = os.path.expanduser('~')
secret_dir = os.path.join(home_dir, 'Google Drive', 'personal-dashboard')
CLIENT_SECRET_FILE = os.path.join(secret_dir, 'client_secret.json')
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """
    Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    :returns: Credentials, the obtained credential.
    """
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print(f'Storing credentials to {credential_path}')
    return credentials


def get_next_events(n=10):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    n events on the user's calendar.

    :param int n: The number of upcoming events to return.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time  # noqa: E501
    events_result = service.events().list(
        calendarId='primary', timeMin=now, maxResults=n, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
