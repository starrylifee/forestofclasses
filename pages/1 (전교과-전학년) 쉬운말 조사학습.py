import streamlit as st
import requests
import toml
import pathlib
import urllib.parse
from bs4 import BeautifulSoup
from openai import OpenAI  # openai 모듈을 임포트합니다.

# 웹페이지 제목 설정
st.set_page_config(
    page_title="함께학교 프로젝트",
    page_icon="🏫"
)

# GitHub 아이콘 숨기기
hide_github_icon = """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK{ display: none; }
    #MainMenu{ visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
"""

st.markdown(hide_github_icon, unsafe_allow_html=True)

# 프로젝트 루트 디렉토리 설정
base_path = pathlib.Path(__file__).parent.parent

# secrets.toml 파일 경로
secrets_path = base_path / ".streamlit" / "secrets.toml"

# secrets.toml 파일 읽기
try:
    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = toml.load(f)
except FileNotFoundError:
    st.error(f"secrets.toml 파일을 찾을 수 없습니다: {secrets_path}")
    st.stop()
except Exception as e:
    st.error(f"secrets.toml 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# OpenAI API 키 설정
api_key = secrets.get("openai_api_key")
if not api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다.")
    st.stop()

# OpenAI 클라이언트 설정
client = OpenAI(api_key=api_key)

# 비밀번호 입력 전 이미지를 보여줌
password = st.text_input("**비밀번호를 입력하세요**:", type="password")

# 비밀번호가 올바르지 않은 경우 이미지 표시
if password != secrets.get("page_password_1"):
    st.image("files/a2.png")  # 이미지 경로는 루트 디렉토리의 files 폴더
    st.stop()

# 비밀번호가 올바른 경우, 원래의 내용 출력
st.title("📖 쉬운말 조사 학습 📖")

# 조사할 주제와 학년 입력 받기
st.header("조사 주제 선택")
st.write("조사하고 싶은 주제를 입력하고 학년을 선택하세요.")
query = st.text_input("조사할 주제")
grade_level = st.selectbox("학년을 선택하세요", options=["초등학교 1~2", "초등학교 3~4", "초등학교 5~6"])

# 네이버 API 키 설정
naver_client_id = secrets.get("naver_client_id")
naver_client_secret = secrets.get("naver_client_secret")

# 네이버 백과사전 검색 함수
def search_naver_encyclopedia(query):
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/encyc.json?query={encText}"
    headers = {
        "X-Naver-Client-Id": naver_client_id,
        "X-Naver-Client-Secret": naver_client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get('items', [])
        return items[0] if items else None
    else:
        return None

# HTML 태그 제거 함수
def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# OpenAI GPT 호출 함수 (학년에 맞춘 번역)
def translate_text(text, grade_level):
    prompt = f"다음 글을 {grade_level} 학년이 이해하기 쉽게 번역해 주세요. 가능한 자세히 번역해 주세요.:\n\n{text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용 가능한 모델로 변경
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=0.7
        )
        message_content = response.choices[0].message.content.strip()
        return message_content
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return "번역 생성에 실패했습니다."

# 검색 버튼 클릭 시 실행
if st.button("검색하기"):
    if query:
        with st.spinner("잠시만 기다리십시오"):
            # 네이버 백과사전 검색
            item = search_naver_encyclopedia(query)
            if item:
                st.header("검색 결과")
                st.write(f"[네이버 페이지로 이동하려면 클릭하세요]({item['link']})")
                
                # 번역된 결과 표시
                original_text = remove_html_tags(item['description'])
                translated_text = translate_text(original_text, grade_level)
                st.write("#### 번역된 내용")
                st.write(translated_text)
            else:
                st.warning("검색 결과가 없습니다.")
    else:
        st.warning("조사할 주제를 입력해주세요!")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.rerun()