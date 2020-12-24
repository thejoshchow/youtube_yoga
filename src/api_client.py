import pymongo
from googleapiclient.discovery import build
import googleapiclient.errors

class youtube():
    def __init__(self, youtube_api, query):
        self.youtube_api = youtube_api
        self.query = query

    def get_video_ids(self, token=None):

        # Returns nextPageToken and videoIds of first page of query with search() function of youtube api

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
    
        # Returns full list of all query items
    
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

    def video_details(self, video):

        # video() method of youtube api returns video metadata for list from grab_videos method

        request = self.youtube_api.videos().list(
            part='snippet, contentDetails, statistics',
            fields = 'items(contentDetails(duration), id, snippet(categoryId, title, description, channelTitle, tags), statistics(commentCount, dislikeCount, likeCount, viewCount))',
            id=video
        ).execute()
        return request


    def main(self):
        print(f'Searching youtube for {self.query}')
        videos = self.grab_videos()
        print(f'Adding {len(videos)} videos to database')
        count = 0
        for video in videos:
            request = self.video_details(video)
            try:
                col.insert_one(request['items'][0])
                print(f'{video[0]} added')
                count += 1
            except pymongo.errors.DuplicateKeyError:
                continue
        print(f'Script complete: {count} videos added.')

    # def test(self):
    #     one_result = col.find_one()
    #     print(f'From MongoDB: {one_result}')
    #     print(' ')
    #     test, test_result = self.get_video_ids()
    #     print(f'Test token: {test}')
    #     print(f'Test query response: {test_result}')
    
    # def new_test(self):
    #     print(self.video_details(self.query))
    #     print(' ')


if __name__ == '__main__':
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = input('API Key: ')
    youtube_api = build(serviceName=api_service_name, version=api_version, developerKey=DEVELOPER_KEY)

    # connect to MongoDB client and create database and collection
    client = pymongo.MongoClient()
    db = client.yoga
    col = db.final

    query1 = ['yoga', 'vinyasa', 'vinyasa yoga', 'vinyasa flow']
    query2 = ['hatha', 'hatha yoga', 'ashtanga', 'ashtanga yoga']
    query3 = ['restorative yoga', 'yin yoga', 'kundalini', 'kundalini yoga']
    query4 = ['prenatal yoga', 'pilates', 'pilates yoga', 'nidra']
    query5 = ['nidra yoga', 'sound bath', 'sound baths']
    query6 = ['mindfulness yoga', 'breathwork', 'mindful yoga']
    query7 = ['breathwork yoga', 'restorative yin', 'yoga flow']

    # single list of queries if you are not limited by api call quota
    queries = query1 + query2 + query3 + query4 + query5 + query6 + query7

    # test_5 = ['np0c-WP8ocE', 'XGr6PICjQz8', 'yEExEFGVCk8', 'Rl42wr9hkPE', 'eCQlyDLsp9Y']

    for query in queries:
        main = youtube(youtube_api, query)
        main.main()
