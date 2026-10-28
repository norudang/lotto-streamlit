
import requests
import streamlit as st
from urllib.parse import urlparse, parse_qs

# API 키 입력
API_KEY = "AIzaSyDRt4MOvf9JcnGmKEipSbRRv1HcOB6o1C8"

# 페이지 설정
st.set_page_config(
    page_title="유튜브 참여율 분석",
    page_icon="📊",
    layout="centered"
)

st.title("📊 유튜브 참여율 분석")
st.write("유튜브 영상의 조회수, 좋아요, 댓글 수를 분석합니다.")

video_url = st.text_input(
    "유튜브 영상 주소를 입력하세요",
    value="https://www.youtube.com/watch?v=34TVs8d1Xhs"
)

def extract_video_id(url):
    url = url.strip()

    if len(url) == 11 and "/" not in url and "?" not in url:
        return url

    parsed = urlparse(url)

    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.strip("/").split("/")[0]

    if parsed.hostname and parsed.hostname.endswith("youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        if parsed.path.startswith(("/embed/", "/shorts/")):
            parts = parsed.path.strip("/").split("/")
            if len(parts) >= 2:
                return parts[1]

    return None

if st.button("🔍 분석하기"):
    video_id = extract_video_id(video_url)

    if not video_id:
        st.error("올바른 유튜브 영상 주소를 입력해 주세요.")

    elif API_KEY == "여기에_API_키_입력":
        st.error("코드 맨 위에 실제 YouTube API 키를 입력해 주세요.")

    else:
        try:
            response = requests.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "part": "snippet,statistics",
                    "id": video_id,
                    "key": API_KEY
                },
                timeout=30
            )

            data = response.json()

            if not response.ok:
                error = data.get("error", {}).get(
                    "message", "알 수 없는 오류"
                )
                st.error(f"YouTube API 오류: {error}")

            elif not data.get("items"):
                st.error("영상을 찾을 수 없습니다.")

            else:
                video = data["items"][0]
                title = video["snippet"]["title"]
                stats = video["statistics"]

                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))

                st.subheader(f"🎬 {title}")

                col1, col2, col3 = st.columns(3)
                col1.metric("조회수", f"{views:,}회")
                col2.metric("좋아요", f"{likes:,}개")
                col3.metric("댓글", f"{comments:,}개")

                st.divider()
                st.subheader("📈 참여율 분석 결과")

                if views > 0:
                    st.metric(
                        "좋아요 비율",
                        f"{likes / views * 100:.2f}%"
                    )
                    st.metric(
                        "댓글 비율",
                        f"{comments / views * 100:.2f}%"
                    )
                    st.metric(
                        "좋아요 + 댓글의 조회수 대비 비율",
                        f"{(likes + comments) / views * 100:.2f}%"
                    )

                    st.caption(
                        "※ 조회수 대비 비율이며, 실제 시청자 중 "
                        "행동한 사람의 비율과는 다를 수 있습니다."
                    )
                else:
                    st.warning("조회수가 0이라 비율을 계산할 수 없습니다.")

        except requests.RequestException:
            st.error("네트워크 오류가 발생했습니다. 다시 시도해 주세요.")

st.divider()
st.caption("YouTube Data API를 이용한 영상 통계 분석")


