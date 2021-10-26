from datetime import timedelta
import  re
import os
from googleapiclient.discovery import build, HttpError

def main():
    #api credentials from https://console.cloud.google.com/apis/credentials/
    # api_key = os.environ.get('YOUTUBE_API_KEY')
    api_key = 'AIzaSyCF-nMsUswu8NYCEtx1JxNoKYTBqgbKcRw'

    youtubeService = build('youtube', 'v3',developerKey = api_key)

    totalVideoSeconds = 0

    #to seprate the hours minutes and seconds from the output of videoResponse
    hoursPattern = re.compile(r'(\d+)H')
    minutesPattern = re.compile(r'(\d+)M')
    secondsPattern = re.compile(r'(\d+)S')

    nextPageToken = None
    
    while True:
        playlistRequest = youtubeService.playlistItems().list(
            #to be used with playlistItems service request
            part = 'contentDetails', 
            
            playlistId='PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O',  # ARCH studio Rhino Tutorials
            #id is for the playlist id unlike the channelId which is clearly for the channel id
            # playlistId='PLdo4fOcmZ0oV2uhlVIItfXxuRXsv-gXD5',  # ARCH studio Rhino Tutorials
            # playlistId = 'PLi01XoE8jYohWFPpC17Z-wWhPOSuh8Er-', #ARCH studio Rhino Tutorials
            maxResults = 50,
            # maxResults = 50,
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

            videoResponse = videoRequest.execute()

            for item in videoResponse['items']:
            
                videoDuration = item['contentDetails']['duration']

                hours = hoursPattern.search(videoDuration) 
                minutes = minutesPattern.search(videoDuration)
                seconds = secondsPattern.search(videoDuration)
                
                hours = int(hours.group(1)) if hours else  0
                minutes = int(minutes.group(1)) if minutes else  0 
                seconds = int(seconds.group(1)) if seconds else  0 

                
                videoSeconds = timedelta(
                    hours = hours, 
                    minutes = minutes, 
                    seconds = seconds
                        ).total_seconds()

                totalVideoSeconds += videoSeconds
           
            
            totalVideoSeconds = int(totalVideoSeconds)
            
            minutes, seconds = divmod(totalVideoSeconds, 60)
            hours, minutes = divmod(minutes, 60)


            nextPageToken = playlistResponse.get('nextPageToken')
            if not nextPageToken:
                break
                

        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    print (f'Total Playlist duration is {hours} Hours {minutes} Minutes {seconds} Seconds.' )
if __name__ == "__main__":
    main()
    
