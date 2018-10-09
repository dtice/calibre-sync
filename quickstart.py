from __future__ import print_function
import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def main():
    """Calibre Library Synchronization"""
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

    # read user data
    with open('data.json') as json_file:
        data = json.load(json_file)

    # Check for remote library using name
    if data['library_name'] == "":
        data['library_name'] = input("What is the name of your library?: ")

    results = service.files().list(
        q="name contains "+"'"+data['library_name']+"'",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Read local library
    if not data['local_library_path']:
        data['local_library_path'] = input("What is the full path to your Calibre Library?: ")

    data['local_library'] = read_local_library(data['local_library_path'])

    # if remote library does not exist or has no files
    if not items:
        # ask user to create remote library folder
        print('No files found. Would you like to create a new calibre backup?')
        if input("(yes/no): ") == "yes":
            # create blank library in root GDrive folder
            file_metadata = {
                'name': data['library_name'],
                'mimeType': 'application/vnd.google-apps.folder'
                }
            library = service.files().create(body=file_metadata, fields='id').execute()
            data['remote_library_id'] = library.get('id')

            # push all files in local calibre library to remote library

        else:
            print("See ya!")
    else:
        # if remote library exists but has not been accessed
        if data['remote_library_id'] == "":
            # search for remote library (assumes unique calibre library name)
            library = items[0]
            print("Library Found")
            data['remote_library_id'] = library.get('id')
            print(data['remote_library_id'])

        # if remote library exists and has been accessed
        else:
            library = service.files().list(
                q="'" + data['remote_library_id'] + "'" + " in parents"
            ).execute()
            authors = library.get('files', [])

            # for each item in remote library
            for author in authors:
                # if it is a folder
                if author['mimeType'] == 'application/vnd.google-apps.folder':
                    # retrieve works by author
                    author_works = service.files().list(
                        q="'"+author['id']+"' in parents"
                    ).execute()
                    books = author_works.get('files', [])
                    # for each book by the author
                    for book in books:
                        # if it is a folder
                        if book['mimeType'] == 'application/vnd.google-apps.folder':
                            # check book name against local library
                            continue

            #    if book does not exist in remote library
                    # push book to remote library

    # write variables to json
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


def read_local_library(path):
    local_library = {}
    for author in os.listdir(path):
        if os.path.isdir(path+"/"+author):
            for book in os.listdir(path+"/"+author):
                local_library[author] = book
    return local_library

if __name__ == '__main__':
    main()
