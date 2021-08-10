import base64
import json
import os

from googleapiclient.discovery import MediaFileUpload, build
from oauth2client.service_account import ServiceAccountCredentials

GOOGLE_SERVICE_ACCOUNT = base64.b64decode(os.environ['GOOGLE_SERVICE_ACCOUNT']).decode('UTF-8')

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(GOOGLE_SERVICE_ACCOUNT),
    scopes=['https://www.googleapis.com/auth/drive']
)

service = build('drive', 'v3', credentials=creds)


def update_file(file_id, path, name):
    file = service.files().get(fileId=file_id).execute()

    del file['id']
    file['name'] = name

    media_body = MediaFileUpload(path, resumable=True)
    service.files().update(fileId=file_id, body=file, media_body=media_body).execute()


update_file(
    '11Z3RAhI97Dan2usiuN5CUWwfJ23WLNob',
    'publisher_analysis_template.ipynb',
    'Publisher Analysis Template'
)
update_file(
    '1NXYvi3eHOWlFHXzcg7Vhw3xNJpNXcqx1',
    'setup_environment.ipynb',
    'Meta Analysis Template'
)
update_file(
    '1GmkA3kFL9k9MdTUln4pcRmc-KZneL5VB',
    'structure_and_format_feedback_template.ipynb',
    'Structure and Format Feedback Template'
)
update_file(
    '1Lj96xTde5GpFQ5hnvB2GYZ7gY4wuvUYt',
    'data_quality_feedback_template.ipynb',
    'Data Quality Feedback Template'
)
