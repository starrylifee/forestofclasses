import streamlit as st

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

# 페이지 제목과 설명
st.title("📚함께학교 수업자료 나눔🏫")
st.write("""
    🎉 **환영합니다!** 함께학교에서 진행하는 **수업자료 나눔 프로젝트**에 오신 것을 환영합니다! 
    이 프로젝트는 다양한 주제의 **AI SW 수업자료**를 생성하고 공유하는 것을 목표로 합니다.
""")
st.write("""
    🔍 **사용 방법:** 왼쪽 상단의 사이드바에서 필요한 도구를 선택해 보세요.🌟
""")

# 카카오톡 문의 링크
st.markdown("""
    💬 **인공지능 도구를 만들고 싶으신가요?**  
    무료로 만들어드립니다. 카카오톡을 통해 문의해 주세요: [카카오톡 문의하기](https://open.kakao.com/o/s7aVgweg)
""")

# 지원 정보
st.write("🛠️ 이 프로젝트는 **서울특별시교육청 AI SW 선도교사**의 활동 지원으로 운영되고 있습니다.")
st.write("🏫 제작 : **서울신답초등학교 정용석**")

# 함께학교 로고 표시
st.image("files/logo.png", use_column_width=True)
