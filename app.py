
import requests
import streamlit as st
from urllib.parse import urlparse, parse_qs

# 페이지 설정
st.set_page_config(
    page_title="유튜브 참여율 분석",
    page_icon="📊",
    layout="centered"
)

# 제목 및 설명
st.title("📊 유튜브 참여율 분석")
st.write("유튜브 영상의 조회수, 좋아요, 댓글 수를 분석합니다.")

# 영상 주소 입력
video_url = st.text_input(
    "유튜브 영상 주소 또는 영상 ID",
    value="https://www.youtube.com/watch?v=34TVs8d1Xhs"
)

def extract_video_id(url):
    url = url.strip()

    # 영상 ID만 입력한 경우
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

# 분석 버튼
if st.button("🔍 분석하기", type="primary"):
    video_id = extract_video_id(video_url)

    if not video_id:
        st.error("올바른 유튜브 영상 주소를 입력해 주세요.")

    else:
        try:
            # Streamlit Cloud Secrets에서 API 키 가져오기
            api_key = st.secrets["YOUTUBE_API_KEY"]

            response = requests.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "part": "snippet,statistics",
                    "id": video_id,
                    "key": api_key
                },
                timeout=30
            )

            data = response.json()

            if not response.ok:
                message = data.get("error", {}).get(
                    "message", "알 수 없는 API 오류"
                )
                st.error(f"YouTube API 오류: {message}")

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

                # 주요 통계
                col1, col2, col3 = st.columns(3)

                col1.metric("조회수", f"{views:,}회")
                col2.metric("좋아요", f"{likes:,}개")
                col3.metric("댓글", f"{comments:,}개")

                st.divider()
                st.subheader("📈 참여율 분석 결과")

                if views > 0:
                    like_rate = likes / views * 100
                    comment_rate = comments / views * 100
                    total_rate = (likes + comments) / views * 100

                    col1, col2 = st.columns(2)

                    col1.metric("좋아요 비율", f"{like_rate:.2f}%")
                    col2.metric("댓글 비율", f"{comment_rate:.2f}%")

                    st.metric(
                        "좋아요 + 댓글의 조회수 대비 비율",
                        f"{total_rate:.2f}%"
                    )

                    st.caption(
                        "※ 조회수 대비 비율이며, 실제 시청자 중 "
                        "행동한 사람의 비율과는 다를 수 있습니다."
                    )
                else:
                    st.warning("조회수가 0이라 비율을 계산할 수 없습니다.")

        except KeyError:
            st.error(
                "API 키가 설정되지 않았습니다. "
                "Streamlit Cloud의 앱 설정에서 Secrets를 등록해 주세요."
            )

        except requests.RequestException:
            st.error("네트워크 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")

        except ValueError:
            st.error("API 응답을 처리할 수 없습니다.")

st.divider()
st.caption("YouTube Data API를 이용한 영상 통계 분석")


