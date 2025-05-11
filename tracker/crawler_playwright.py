from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from .models import CharacterRanking

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# def crawl_character_playwright(character_name, specific_server=None, try_all_servers=False):
#     logger = logging.getLogger(__name__)
    
#     servers = (
#         ["데이안", "아이라", "던컨", "알리사", "메이븐", "라사", "칼릭스"]
#         if try_all_servers else [specific_server or "데이안"]
#     )
    
#     result = None

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto("https://mabinogimobile.nexon.com/Ranking/List?t=1")

#         for server in servers:
#             try:
#                 logger.info(f"[{server}] 서버 검색 중...")
                
#                 # 서버 선택
#                 page.click("div.select_box[data-mm-selectbox]")
#                 page.wait_for_timeout(300)
#                 page.click(f"li:has-text('{server}')")
#                 page.wait_for_timeout(500)

#                 # 검색어 입력
#                 page.fill("input[name='search']", character_name)
#                 page.click("button.search_button")
#                 page.wait_for_timeout(3000)

#                 soup = BeautifulSoup(page.content(), "html.parser")
                
#                 # data-charactername 속성 기준으로 정확히 찾음
#                 char_tag = soup.select_one(f'dd[data-charactername="{character_name}"]')
#                 if not char_tag:
#                     logger.info(f"캐릭터 '{character_name}' 없음")
#                     continue

#                 # 상위 li 블록
#                 li_block = char_tag.find_parent("li")
#                 if not li_block:
#                     continue

#                 # 정보 추출
#                 combat_power = li_block.select_one("dd.type_1")
#                 # char_class = li_block.select_one("dl:has(dt:contains('클래스')) dd")
#                 char_class = li_block.select_one("dl:has(dt:-soup-contains('클래스')) dd")

#                 result = {
#                     "server": server,
#                     "character_class": char_class.text.strip() if char_class else "알 수 없음",
#                     "class_code": char_class.get("class", [""])[0] if char_class else "",
#                     "combat_power": int(combat_power.text.replace(",", "")) if combat_power else 0
#                 }

#                 logger.info(f"결과: {result}")
#                 break  # 찾았으면 종료

#             except Exception as e:
#                 logger.error(f"서버 '{server}' 검색 오류: {e}")

#         browser.close()

#     return result


# def crawl_all_streamers_playwright(streamers):
#     """모든 스트리머 캐릭터 크롤링 """
#     results = []
    
#     for streamer in streamers:
#         # 서버 정보가 있으면 해당 서버에서 먼저 검색
#         result = crawl_character_playwright(
#             streamer.character_name, 
#             specific_server=streamer.server,
#             try_all_servers=False
#         )
        
#         # 찾지 못했다면 모든 서버에서 검색
#         if not result:
#             logger.warning(f"스트리머 {streamer.streamer_name}의 캐릭터를 지정된 서버에서 찾지 못했습니다. 모든 서버에서 검색합니다.")
#             result = crawl_character_playwright(
#                 streamer.character_name, 
#                 try_all_servers=True
#             )
        
#         if result:
#             result['streamer'] = streamer
#             results.append(result)
            
#             # 서버 정보가 변경되었다면 업데이트
#             if result['server'] != streamer.server:
#                 logger.info(f"서버 정보 업데이트: {streamer.server} -> {result['server']}")
#                 streamer.server = result['server']
#                 streamer.save()
                
#             logger.info(f"{streamer.streamer_name}의 캐릭터 {streamer.character_name} 정보 추출 성공")
#         else:
#             logger.warning(f"{streamer.streamer_name}의 캐릭터 {streamer.character_name} 정보를 찾을 수 없습니다.")
    
#     return results

def crawl_character_playwright(character_name, specific_server):
    logger = logging.getLogger(__name__)
    
    result = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://mabinogimobile.nexon.com/Ranking/List?t=1")

        try:
            logger.info(f"[{specific_server}] 서버 검색 중...")
            
            # 서버 선택
            page.click("div.select_box[data-mm-selectbox]")
            page.wait_for_timeout(300)
            page.click(f"li:has-text('{specific_server}')")
            page.wait_for_timeout(500)

            # 검색어 입력
            page.fill("input[name='search']", character_name)
            page.click("button.search_button")
            page.wait_for_timeout(3000)

            soup = BeautifulSoup(page.content(), "html.parser")
            
            # data-charactername 속성 기준으로 정확히 찾음
            char_tag = soup.select_one(f'dd[data-charactername="{character_name}"]')
            if not char_tag:
                logger.info(f"캐릭터 '{character_name}' 없음")
                return None

            # 상위 li 블록
            li_block = char_tag.find_parent("li")
            if not li_block:
                return None

            # 정보 추출
            combat_power = li_block.select_one("dd.type_1")
            char_class = li_block.select_one("dl:has(dt:-soup-contains('클래스')) dd")

            result = {
                "server": specific_server,
                "character_class": char_class.text.strip() if char_class else "알 수 없음",
                "class_code": char_class.get("class", [""])[0] if char_class else "",
                "combat_power": int(combat_power.text.replace(",", "")) if combat_power else 0
            }

            logger.info(f"결과: {result}")

        except Exception as e:
            logger.error(f"서버 '{specific_server}' 검색 오류: {e}")

        browser.close()

    return result


def crawl_all_streamers_playwright(streamers):
    """모든 스트리머 캐릭터 크롤링 """
    results = []
    
    for streamer in streamers:
        # 지정된 서버에서만 검색
        result = crawl_character_playwright(
            streamer.character_name, 
            specific_server=streamer.server,
        )
        
        if result:
            result['streamer'] = streamer
            results.append(result)
            
            # 서버 정보가 변경되었다면 업데이트 (필요하면 유지)
            if result['server'] != streamer.server:
                logger.info(f"서버 정보 업데이트: {streamer.server} -> {result['server']}")
                streamer.server = result['server']
                streamer.save()
                
            logger.info(f"{streamer.streamer_name}의 캐릭터 {streamer.character_name} 정보 추출 성공")
        else:
            logger.warning(f"{streamer.streamer_name}의 캐릭터 {streamer.character_name} 정보를 찾을 수 없습니다.")
    
    return results