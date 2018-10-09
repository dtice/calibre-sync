from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Check if user has a calibre_sync_library folder on their root GDrive

    # Example
    # Call the Drive v3 API
    # calibre_sync_remote_file_id = get_remote_sync_file_id()
    # library_name = input("Enter the name of your calibre_sync_library: ")

    # json io
    with open('data.json') as json_file:
        data = json.load(json_file)
        remote_library_id = data["remote_library_id"]
        local_library_path = data["local_library_path"]
        library_name = data["library_name"]

    # Check for remote library
    library_name = raw_input("What is the name of your library?: ")
    results = service.files().list(
        q="name contains "+"'"+library_name+"'",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # if remote library does not exist
    if not items:
        # ask user to create remote library folder
        print('No files found. Would you like to create a new calibre backup?')
        if raw_input("(yes/no): ") == "yes":
            # create blank library in root GDrive folder
            file_metadata = {
                'name': library_name,
                'mimeType': 'application/vnd.google-apps.folder'
                }
            library = service.files().create(body=file_metadata, fields='id').execute()
            remote_library_id = library.get('id')

            # push all files in local calibre library to remote library

        else:
            print("See ya!")
            exit
    else:
        # if remote library exists but has not been accessed
        if remote_library_id == "":
            # search for remote library (assumes unique calibre library name)
            library = items[0]
            print("Library Found")
            remote_library_id = library.get('id')
            print(remote_library_id)

        # if remote library exists and has been accessed
        else:
            library = service.files().get(fileId=remote_library_id).execute()

    # TODO write variables to json


if __name__ == '__main__':
    main()
