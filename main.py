import os
from googleapiclient.discovery import build

#api credentials from https://console.cloud.google.com/apis/credentials/
api_key = os.environ.get('YOUTUBE_API_KEY')


youtubeService = build('youtube', 'v3',developerKey = api_key)

request = youtubeService.channels().list(
    part = 'statstics',
    forUsername = '5hM4vtu-38xi_PdX_anGPw'
)
response = request.execute()

#check if the key is valid
print(api_key)

