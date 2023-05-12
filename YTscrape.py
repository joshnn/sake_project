import requests
import urllib.parse as parse
import csv

API_KEY = "AIzaSyCOllEKMNxFSbWDISAORovtVG_wvyGAQBw"
URL_HEAD = "https://www.googleapis.com/youtube/v3/commentThreads?"
URL_HEAD = "https://www.youtube.com/watch?v=bqigIHMComE&"
URL_HEAD = "https://youtube.googleapis.com/youtube/v3/comments?" # part=snippet&id=bqigIHMComE&textFormat=plainText&key=[YOUR_API_KEY] HTTP/1.1

nextPageToken = ''
item_count = 0
items_output = [    
    ['videoId']+
    ['textDisplay']+
    ['textOriginal']+
    ['authorDisplayName']+
    ['authorProfileImageUrl']+
    ['authorChannelUrl']+
    ['authorChannelId']+
    ['canRate']+
    ['viewerRating']+
    ['likeCount']+
    ['publishedAt']+
    ['updatedAt']
]
#パラメータ設定
video_id = "v=bqigIHMComE"
channelId = "xxx"
exe_num = 1

for i in range(exe_num):

    #APIパラメータセット
    param = {
        'key':API_KEY,
        'part':'snippet',
        #----↓フィルタ（いずれか1つ）↓-------
        'id':channelId,
        'videoId':video_id,
        #----↑フィルタ（いずれか1つ）↑-------
        #'maxResults':'100',
        #'moderationStatus':'published',
        #'order':'relevance',
        #'pageToken':nextPageToken,
        #'searchTerms':'',
        'textFormat':'plainText',
    }
    #リクエストURL作成
    target_url = URL_HEAD + (parse.urlencode(param))

    #データ取得
    res = requests.get(target_url).json()

    #件数
    item_count += len(res['items'])
#print(target_url)
    print(str(item_count)+"件")

#コメント情報を変数に格納
    for item in res['items']:
        items_output.append(
            [str(item['snippet']['topLevelComment']['snippet']['videoId'])]+
            [str(item['snippet']['topLevelComment']['snippet']['textDisplay'].replace('\n', ''))]+
            [str(item['snippet']['topLevelComment']['snippet']['textOriginal'])]+
            [str(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])]+
            [str(item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])]+
            [str(item['snippet']['topLevelComment']['snippet']['authorChannelUrl'])]+
            [str(item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])]+
            [str(item['snippet']['topLevelComment']['snippet']['canRate'])]+
            [str(item['snippet']['topLevelComment']['snippet']['viewerRating'])]+
            [str(item['snippet']['topLevelComment']['snippet']['likeCount'])]+
            [str(item['snippet']['topLevelComment']['snippet']['publishedAt'])]+
            [str(item['snippet']['topLevelComment']['snippet']['updatedAt'])]
        ) 

#nextPageTokenがなくなったら処理ストップ
    if 'nextPageToken' in res:
        nextPageToken = res['nextPageToken']
    else:
        break

#CSVで出力
f = open('youtube-comments-list.csv', 'w', newline='', encoding='UTF-8')
writer = csv.writer(f)
writer.writerows(items_output)
f.close()