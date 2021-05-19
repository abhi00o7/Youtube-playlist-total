import os
from googleapiclient.discovery import build
from googleapiclient.discovery import HttpError

def main():
    #api credentials from https://console.cloud.google.com/apis/credentials/
    api_key = os.environ.get('YOUTUBE_API_KEY')


    youtubeService = build('youtube', 'v3',developerKey = api_key)

    playlistRequest = youtubeService.playlists().list(
        part = 'contentDetails',
        id = 'UCiEy6COjB-UVOwdn6qIovhw'
    )

    try:
        response = playlistRequest.execute()
        for item in playlistRequest['items']:
            print(item,"\n")
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

if __name__ == "__main__":
    main()
