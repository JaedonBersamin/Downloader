import os
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import traceback  # Import traceback for detailed error messages

# Set up your OAuth 2.0 credentials
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
CLIENT_SECRETS_FILE = 'client_secret.json'

# Directory path to save downloaded photos
SAVE_DIRECTORY = r''

def authenticate():
    try:
        print("Loading client secrets file...")
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        print("Client secrets loaded successfully.")
        credentials = flow.run_local_server(port=0)
        print("Credentials obtained.")
        return credentials
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        raise

def create_service(credentials):
    try:
        service = googleapiclient.discovery.build('photoslibrary', 'v1', credentials=credentials, static_discovery=False)
        print("Google Photos service created successfully.")
        return service
    except Exception as e:
        print(f"Failed to create Google Photos service: {e}")
        traceback.print_exc()  # Print the traceback for detailed error analysis
        raise

def download_photos(service):
    nextPageToken = None

    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

    while True:
        try:
            results = service.mediaItems().list(pageSize=100, pageToken=nextPageToken).execute()
            items = results.get('mediaItems', [])

            for item in items:
                file_name = os.path.join(SAVE_DIRECTORY, item['filename'])

                # Check if the item is an image or a video
                if 'image' in item['mimeType']:
                    download_url = item['baseUrl'] + '=d'
                elif 'video' in item['mimeType']:
                    download_url = item['baseUrl'] + '=dv'
                else:
                    print(f'Skipping {item["filename"]} due to unsupported type: {item["mimeType"]}')
                    continue

                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(file_name, 'wb') as f:
                        f.write(response.content)
                    print(f'Downloaded {file_name}')
                else:
                    print(f'Failed to download {file_name}')

            nextPageToken = results.get('nextPageToken')
            if not nextPageToken:
                break
        except Exception as e:
            print(f"An error occurred while downloading photos: {e}")
            break

def main():
    try:
        credentials = authenticate()
        service = create_service(credentials)
        download_photos(service)
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == '__main__':
    main()
