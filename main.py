import os
from googleapiclient.discovery import build
from googleapiclient.discovery import HttpError

def main():
    #api credentials from https://console.cloud.google.com/apis/credentials/
    api_key = os.environ.get('YOUTUBE_API_KEY')

    youtubeService = build('youtube', 'v3',developerKey = api_key)

    playlistRequest = youtubeService.playlistItems().list(
        #to be used with playlistItems service request
        part = 'contentDetails',
        # #to be used with playlist service request
        # part = 'contentDetails,snippet, status,id,localizations',
        # #to be used with channel service request
        # part = 'statistics, contentDetails',
        
        #id is for the playlist id unlike the channelId which is clearly for the channel id
        playlistId = 'PLwmnvKn5GXQ9mGUp5uyHddT6jCHtoZ9K_'
        # #ARCH studio 
        # channelId = 'UCiEy6COjB-UVOwdn6qIovhw',
        # #corey schafer
        # channelId = 'UCCezIgC97PvUuR4_gbFUs5g' 
        # #the school of life
        # channelId = 'UC7IcJI8PUf5Z3zKxnZvTBog' 
    )
    
    try:
        playlistResponse = playlistRequest.execute()

        videoIds =[]

        for item in playlistResponse['items']:
            videoIds.append(item['contentDetails']['videoId'])
        
        
        videoRequest = youtubeService.videos().list(
            part = 'contentDetails',
            id = ','.join(videoIds)
        )

        videoDuration =[]
        videoResponse = videoRequest.execute()
        for item in videoResponse['items']:
            videoDuration.append(item['contentDetails']['duration'])
        print(videoDuration)

    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

if __name__ == "__main__":
    main()
