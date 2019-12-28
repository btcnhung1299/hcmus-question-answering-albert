# Init setup
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

def upload(folder_dir, folder_name):
   file_compress = folder_name + '.zip'
   os.system('zip -r {} {}'.format(file_compress, folder_dir))
   new_file = drive.CreateFile({'title': file_compress})
   new_file.SetContentFile(file_compress)
   new_file.Upload()
   print('Uploaded {} to drive'.format(folder_name))
