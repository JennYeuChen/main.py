import os
import requests
from datetime import datetime

# 環境變數設定
YT_API_KEY = os.environ['YT_API_KEY']
NOTION_TOKEN = os.environ['NOTION_TOKEN']
BLOCK_ID = os.environ['NOTION_BLOCK_ID']
CHANNEL_ID = "UCs6o9uBZeQFeULoH9Q-V3pg"

def get_shorts_views():
    total_views = 0
    # 1. 搜尋 8/5 後的影片 (order=date)
    search_url = f"https://www.googleapis.com/youtube/v3/search?key={YT_API_KEY}&channelId={CHANNEL_ID}&part=snippet&type=video&publishedAfter=2026-08-05T00:00:00Z&maxResults=50"
    res = requests.get(search_url).json()
    video_ids = [item['id']['videoId'] for item in res['items']]
    
    # 2. 獲取詳細觀看數
    video_url = f"https://www.googleapis.com/youtube/v3/videos?key={YT_API_KEY}&part=statistics&id={','.join(video_ids)}"
    stats = requests.get(video_url).json()
    
    for item in stats['items']:
        total_views += int(item['statistics']['viewCount'])
    return total_views

def update_notion(views):
    url = f"https://api.notion.com/v1/blocks/{BLOCK_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": f"8/5 後 Shorts 累積觀看數: {views:,}"}}]
        }
    }
    requests.patch(url, headers=headers, json=data)

if __name__ == "__main__":
    views = get_shorts_views()
    update_notion(views)
