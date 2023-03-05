from __future__ import print_function
import pickle
import os.path
from tabulate import tabulate
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']

def get_gdrive_service():
    creds = None
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
    return build('drive', 'v3', credentials=creds)


# def update_file(service, file_id, new_title, new_description, new_mime_type,
#                 new_filename, new_revision):
#   """Update an existing file's metadata and content.

#   Args:
#     service: Drive API service instance.
#     file_id: ID of the file to update.
#     new_title: New title for the file.
#     new_description: New description for the file.
#     new_mime_type: New MIME type for the file.
#     new_filename: Filename of the new content to upload.
#     new_revision: Whether or not to create a new revision for this file.
#   Returns:
#     Updated file metadata if successful, None otherwise.
#   """
#   try:
#     # First retrieve the file from the API.
#     file = service.files().get(fileId=file_id).execute()

#     # File's new metadata.
#     file['title'] = new_title
#     file['description'] = new_description
#     file['mimeType'] = new_mime_type

#     # File's new content.
#     media_body = MediaFileUpload(
#         new_filename, mimetype=new_mime_type, resumable=True)

#     # Send the request to the API.
#     updated_file = service.files().update(
#         fileId=file_id,
#         body=file,
#         newRevision=new_revision,
#         media_body=media_body).execute()
#     return updated_file
#   except errors.HttpError, error:
#     print 'An error occurred: %s' % error
#     return None


def upload_files():
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {
        "name": "TestFolder", # Can input name of new folder HERE
        "mimeType": "application/vnd.google-apps.folder" # Specifies type??
    }
    # create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    # get the folder id
    folder_id = file.get("id")
    print("Folder ID:", folder_id)
    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": "test.txt",
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload("test.txt", resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File created, id:", file.get("id"))
    

def search(service, query):
    # search for the file
    result = []
    page_token = None
    while True:
        response = service.files().list(q=query,
                                        spaces="drive",
                                        fields="nextPageToken, files(id, name, mimeType)",
                                        pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            result.append((file["id"], file["name"], file["mimeType"]))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result
    


def showCurrentDirectory():
    
    service = get_gdrive_service()
    root_folder = service.files().get(fileId='root', fields='name').execute()
    print('Current directory:', root_folder['name'])
    # List all files and folders in the current directory
    results = service.files().list(q="'root' in parents and trashed = false", fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    if not items:
        print('No files or folders found.')
    else:
        print('Files and folders:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['mimeType']))
    
def createDirectory(name):
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder" # Specifies type
    }
    # create the folder
    service.files().create(body=folder_metadata, fields="id").execute()
    return


if __name__ == '__main__':
    showCurrentDirectory()