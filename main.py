from __future__ import print_function
import datetime
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

CurrentDirectoryID = None

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/documents']

def get_gdrive_service():
    creds = None
    global CurrentDirectoryID
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    service = build('drive', 'v3', credentials=creds)
    if CurrentDirectoryID is None:
        root_folder = service.files().get(fileId='root', fields='id').execute()
        CurrentDirectoryID = root_folder['id']
    return service

def get_gdocs_service():
    creds = None
    global CurrentDirectoryID
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    service = build('docs', 'v1', credentials=creds)
    if CurrentDirectoryID is None:
        root_folder = service.files().get(fileId='root', fields='id').execute()
        CurrentDirectoryID = root_folder['id']
    return service


def upload_files(name):
    # authenticate account
    service = get_gdrive_service()
    
    
    file_metadata = {
        "name": name,
        "parents": [CurrentDirectoryID]
    }
    # upload
    media = MediaFileUpload(name, resumable=True) #May need file path
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file['id']
    
def createDoc(name):
    service = get_gdrive_service()
    global CurrentDirectoryID
    
    file_metadata = {
    'name': name,
    'parents': [CurrentDirectoryID],
    'mimeType': 'application/vnd.google-apps.document'
    } 
    file = service.files().create(body=file_metadata).execute()
    return file['id']

def getParentDirectory():
    
    service = get_gdrive_service()
    global CurrentDirectoryID
    file = service.files().get(fileId=CurrentDirectoryID, fields='parents').execute()
    return file.get('parents')[0]


def showCurrentDirectory():
    
    service = get_gdrive_service()
    global CurrentDirectoryID
    query = "'{}' in parents".format(CurrentDirectoryID)

    try:
        # retrieve all files in the folder using the files().list() method
        results = service.files().list(q="parents='"+CurrentDirectoryID+"' and trashed=false",fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])
        
        # print file information for each file in the folder
        directory = []
        for item in items:
            directory.append(f'NAME: {item["name"]} -> TYPE: {item["mimeType"]}')
            print(f'NAME: {item["name"]} -> TYPE: {item["mimeType"]}')
        return directory
            
    except HttpError as error:
        print(f'An error occurred: {error}')
    
def createDirectory(name):
    # authenticate account
    global CurrentDirectoryID
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {
        "name": name,
        'parents': [CurrentDirectoryID],
        "mimeType": "application/vnd.google-apps.folder" # Specifies type
    }
    # create the folder
    service.files().create(body=folder_metadata, fields="id").execute()
    return


def query(FILE_NAME):
    # Build the Drive API client
    service = get_gdrive_service()
    global CurrentDirectoryID

    # Search for the file by name
    if ".txt" in FILE_NAME:
        query = "name='{}' and mimeType='text/plain' and trashed = false and parents='{}'".format(FILE_NAME, CurrentDirectoryID)
    else:
        query = "name='{}' and mimeType='application/vnd.google-apps.document' and trashed = false and parents='{}'".format(FILE_NAME, CurrentDirectoryID)
     
    response = service.files().list(q=query, fields='nextPageToken, files(id, name)').execute()

    # Check if a file was found
    files = response.get('files', [])
    if not files:
        print('File not found in current directory')
        return None
    else:
        # Print the ID of the first file found
        return files[0]['id']


def export_pdf(nameDoc):    
    file = query(nameDoc)
    if (file is None):
        return
    try:
        service = get_gdrive_service()
        request = service.files().export_media(fileId=file, mimeType='application/pdf')
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
        with open(nameDoc + '.pdf', 'wb') as f:
            f.write(file.getbuffer())
        print('Download Complete!')
    except HttpError as error:
        print(f'An error occurred: {error}')
        
def setDirectory(name):
    global CurrentDirectoryID
    service = get_gdrive_service()
    query = "mimeType='application/vnd.google-apps.folder' and trashed=false and name='%s' and '%s' in parents" % (name, CurrentDirectoryID)
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('Folder not found')
        return
    else:
        CurrentDirectoryID = items[0]['id']
        return CurrentDirectoryID


def updateDoc(name):
    file_id = query(name)
    global CurrentDirectoryID
    # Get the ID of the Google Doc to update
    doc_id = file_id

    # Create a connection to the Docs API
    docs_service = get_gdocs_service()


    # Create the request to insert the newline
    dt = datetime.datetime.now()
    date_part = dt.date()
    formatted_date = date_part.strftime('%d-%m-%Y')
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': f"{formatted_date}\n"
            }
        }
    ]

    # Execute the request to insert the newline
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()


if __name__ == '__main__':
    # showCurrentDirectory()
    # setDirectory("YO")
    # getParentDirectory()
    # createDoc("Assignment1")
    # showCurrentDirectory()
    # append_date_to_google_doc(query("Assignment1"))
    # export_pdf("Assignment1")
    
