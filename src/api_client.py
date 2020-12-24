import pymongo
from googleapiclient.discovery import build
import googleapiclient.errors

class youtube():
    def __init__(self, youtube_api, query):
        self.youtube_api = youtube_api
        self.query = query

    def get_video_ids(self, token=None):
        search_response = self.youtube_api.search().list(
            q=self.query,
            type='video',
            pageToken=token,
            order='relevance',
            part='id, snippet',
            fields='nextPageToken,items(id(videoId),snippet(title))',
            relevanceLanguage='en',
            maxResults=50
            ).execute()
        
        videos = []
        
        for search_result in search_response.get('items', []):
            videos.append([search_result['id']['videoId'], search_result['snippet']['title']])
        try:
            nexttok = search_response['nextPageToken']
            return(nexttok, videos)
        except:
            nexttok = 'last_page'
            return(nexttok, videos)

    def grab_videos(self, token=None, max_results=10000):
        out = []
        while len(out) < max_results:
            res = self.get_video_ids(token)
            token = res[0]
            videos = res[1]
            if videos:
                for vid in videos:
                    out.append(vid)
                print("added " + str(len(videos)) + " videos to a total of " + str(len(out)))
            else:
                break
        return out

    def video_details(self):
        print(f'Searching youtube for {self.query}')
        videos = self.grab_videos()
        print(f'Adding {len(videos)} videos to database')
        count = 0
        for video in videos:
            request = self.youtube_api.videos().list(
                part='snippet, contentDetails, statistics',
                fields = 'items(contentDetails(duration), id, snippet(categoryId, title, description, channelTitle), statistics(commentCount, dislikeCount, likeCount, viewCount))',
                id=video
            ).execute()
            try:
                col.insert_one(request['items'][0])
                print(f'{video} added')
                count += 1
            except pymongo.errors.DuplicateKeyError:
                continue
        print(f'Script complete: {count} videos added.')

    def test(self):
        one_result = col.find_one()
        print(f'From MongoDB: {one_result}')
        test, test_result = self.get_video_ids()
        print(f'Test token: {test}')
        print(f'Test query response: {test_result}')


if __name__ == '__main__':
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = input('API key: ')
    youtube_api = build(serviceName=api_service_name, version=api_version, developerKey=DEVELOPER_KEY)

    #connect to MongoDB client and create database and collection
    client = pymongo.MongoClient()
    db = client.yoga
    col = db.videos

    query = 'yin yoga'

    youtube = youtube(youtube_api, query)
    youtube.video_details()
