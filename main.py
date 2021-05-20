from datetime import timedelta
import  re
import os
from googleapiclient.discovery import build, HttpError

def main():
    #api credentials from https://console.cloud.google.com/apis/credentials/
    api_key = os.environ.get('YOUTUBE_API_KEY')

    youtubeService = build('youtube', 'v3',developerKey = api_key)

    nextPageToken = None

    totalVideoSeconds = 0
    #to seprate the hours minutes and seconds from the output of videoResponse
    hoursPattern = re.compile(r'(\d+)H')
    minutesPattern = re.compile(r'(\d+)M')
    secondsPattern = re.compile(r'(\d+)S')

    while True:
        playlistRequest = youtubeService.playlistItems().list(
            #to be used with playlistItems service request
            part = 'contentDetails',
            # #to be used with playlist service request
            # part = 'contentDetails,snippet, status,id,localizations',
            # #to be used with channel service request
            # part = 'statistics, contentDetails',
            
            #id is for the playlist id unlike the channelId which is clearly for the channel id
            playlistId = 'PLwmnvKn5GXQ9mGUp5uyHddT6jCHtoZ9K_',
            #school of life playlist
            # playlistId = 'PLwxNMb28XmpckOvZZ_AZjD7WM2p9-6NBv',
             
            # channelId = 'UCiEy6COjB-UVOwdn6qIovhw',#ARCH studio 
            
            # channelId = 'UCCezIgC97PvUuR4_gbFUs5g' #corey schafer

            # channelId = 'UC7IcJI8PUf5Z3zKxnZvTBog' #the school of life
            maxResults = 50,
            pageToken = nextPageToken
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

            # videoDuration =[]
            videoResponse = videoRequest.execute()

            for item in videoResponse['items']:
            
                videoDuration = item['contentDetails']['duration']
                # videoDuration.append(item['contentDetails']['duration'])
                hours = hoursPattern.search(videoDuration) 
                minutes = minutesPattern.search(videoDuration)
                seconds = secondsPattern.search(videoDuration)
                
                hours = int(hours.group(1)) if hours else  0
                minutes = int(minutes.group(1)) if minutes else  0 
                seconds = int(seconds.group(1)) if seconds else  0 

                
                videoSeconds = timedelta(hours = hours, minutes = minutes, seconds = seconds).total_seconds()
                totalVideoSeconds += videoSeconds
            
            totalVideoSeconds = int(totalVideoSeconds)
            minutes, seconds = divmod(totalVideoSeconds, 60)
            hours, minutes = divmod(minutes, 60)

            print(f'Total Playlist duration is {hours} Hours {minutes} Minutes {seconds} Seconds.' '\n')

            nextPageToken = playlistResponse.get('nextPageToken')
            if not nextPageToken:
                break


        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

if __name__ == "__main__":
    main()
