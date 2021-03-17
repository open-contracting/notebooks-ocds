import os
import json
from googleapiclient.discovery import build, MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT']),
    scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

def update_file(file_id, path, name):

    file = service.files().get(fileId=file_id).execute()

    del file['id']
    file['name'] = name

    media_body = MediaFileUpload(path, resumable=True)

    service.files().update(
        fileId=file_id,
        body=file,
        media_body=media_body).execute()

update_file('1R-VBYA-SC9CoMIdvYp_SI9V2UFWlTqx0', 'kingfisher_analysis_template.ipynb', 'Kingfisher Analysis Template')
