This program uses the google photos api to make it easier to download your photos from Google Photos to your local computer. 
It downloads .mp4, .mov, .jpg, .png, .heic, etc. and directs them towards the directory provided in the python code.


It currently runs locally with a specific google api linked to a specific google account. 

Changes needed to be made by the user:
  - Required python extensions to run the code
  - Input their own Google api "client_secrets.json" file provided to them from Google Photos API
  - Input their desired directory on their system for files to be downloaded to (Line 13:: SAVE_DIRECTORY = r'')

