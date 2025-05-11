# MobiChzzk

치지직 스트리머들의 마비노기 모바일 캐릭터 랭킹 트래커입니다.

## 주요 기능

- 스트리머 캐릭터 정보 관리
- 전투력 랭킹 자동 크롤링 및 추적
- 랭킹 목록 웹 인터페이스 제공

## 기술 스택

- Django 5.2
- Playwright
- BeautifulSoup4

## 설치 방법

```bash
# 저장소 클론
git clone https://github.com/bm4706/mobichzzk.git
cd mobichzzk

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install chromium

# .env 파일 설치해야합니다! 
설치하고 아래 3줄을 넣고 원하시는대로 지정하시면 됩니다!

SECRET_KEY = 'example_key'
DJANGO_ADMIN_URL=example/
DJANGO_CRAWLER_URL=example2/


# 데이터베이스 마이그레이션
python manage.py migrate

# 실행
python manage.py runserver