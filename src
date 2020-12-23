from googleapiclient.discovery import build
import googleapiclient.errors
from pymongo import MongoClient

client = MongoClient()
db = client.yoga
col = db.videos

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyC81m2ul4GD2VSD4259vZeB4bWjomBHAHk"

youtube = build(serviceName='youtube', version='v3', developerKey=DEVELOPER_KEY)

# function for youtube search
def youtube_search(q, max_results=50, order="relevance", token=None, client=youtube):

    youtube = client

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result['id']['videoId'])
    try:
        nexttok = search_response["nextPageToken"]
        return(nexttok, videos)
    except Exception as e:
        print(e.message)
        nexttok = "last_page"
        return(nexttok, videos)

# create list of video ids associated with query
def grab_videos(keyword, token=None, max_results=50):
    out = []
    while len(out) < max_results:
        res = youtube_search(keyword, token=token)
        token = res[0]
        videos = res[1]
        if videos:
            for vid in videos:
                out.append(vid)
            print("added " + str(len(videos)) + " videos to a total of " + str(len(out)))
        else:
            break
    print(token)
    return out

def video_details(videos=None, client=youtube):
    youtube = client
    for video in videos:
        try:
            request = youtube.videos().list(
                part='snippet, contentDetails, statistics',
                id=video
            )
            response = request.execute()
            insert_doc = {'id': response['items'][0]['id'], 'categoryId': response['items'][0]['snippet']['categoryId'], 'description': response['items'][0]['snippet']['description'], 'title': response['items'][0]['snippet']['title'], 'tags': response['items'][0]['snippet']['tags'], 'duration': response['items'][0]['contentDetails']['duration'], 'commentCount': response['items'][0]['statistics']['commentCount'], 'dislikeCount': response['items'][0]['statistics']['dislikeCount'], 'likeCount': response['items'][0]['statistics']['likeCount'], 'viewCount': response['items'][0]['statistics']['viewCount']}
            col.insert_one(insert_doc)
            print('{} added'.format(video))
        except:
            print(f'Failed videoId: {video}')

if __name__ == '__main__':
    videos = grab_videos('yoga', max_results=1000)
    video_details(videos)