import os

#api credentials from https://console.cloud.google.com/apis/credentials/
API_KEY = os.environ.get('YOUTUBE_API_KEY')

#check if the key is valid
print(API_KEY)
