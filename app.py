
import requests
import streamlit as st

API_KEY = st.secrets["YOUTUBE_API_KEY"]
VIDEO_ID = "34TVs8d1Xhs"

# 2. 영상 통계 가져오기
url = "https://www.googleapis.com/youtube/v3/videos"

params = {
    "part": "snippet,statistics",
    "id": VIDEO_ID,
    "key": API_KEY
}

response = requests.get(url, params=params, timeout=30)
data = response.json()

if not response.ok:
    print("API 오류:", data.get("error", {}).get("message"))

elif not data.get("items"):
    print("영상을 찾을 수 없습니다.")

else:
    video = data["items"][0]
    title = video["snippet"]["title"]
    stats = video["statistics"]

    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))

    print("=" * 45)
    print("📊 유튜브 참여율 분석")
    print("=" * 45)
    print("영상 제목:", title)
    print(f"조회수: {views:,}회")
    print(f"좋아요 수: {likes:,}개")
    print(f"댓글 수: {comments:,}개")

    if views > 0:
        like_rate = likes / views * 100
        comment_rate = comments / views * 100
        total_rate = (likes + comments) / views * 100

        print("-" * 45)
        print(f"좋아요 비율: {like_rate:.2f}%")
        print(f"댓글 비율: {comment_rate:.2f}%")
        print(f"좋아요 또는 댓글 수 합계의 조회수 대비 비율: {total_rate:.2f}%")
    else:
        print("조회수가 0이므로 비율을 계산할 수 없습니다.")

    print("=" * 45)
    print("※ 실제 시청자 중 행동한 사람의 비율과는 다를 수 있습니다.")

