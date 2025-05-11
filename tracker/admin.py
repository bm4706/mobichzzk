# tracker/admin.py
from django.contrib import admin
from django.contrib import messages
from .models import StreamerCharacter, CharacterRanking
from .crawler_playwright import crawl_all_streamers_playwright
import json
import os
from datetime import datetime

# 데이터를 JSON으로 저장하는 함수
def save_to_json(data, filename="rankings.json"):
    """데이터를 JSON 파일로 저장"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True, filename
    except Exception as e:
        return False, str(e)


# 2. 현재 데이터 JSON으로 내보내기 액션
@admin.action(description="현재 랭킹 데이터를 JSON으로 내보내기")
def export_to_json(modeladmin, request, queryset):
    try:
        # 현재 모델 타입 확인
        if modeladmin.model == CharacterRanking:
            # CharacterRanking에서 호출했을 경우
            if queryset.exists():
                rankings = queryset
                filename = f"selected_rankings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                rankings = CharacterRanking.objects.all()
                filename = f"all_rankings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # 데이터 수집
            export_data = []
            for ranking in rankings:
                streamer = ranking.streamer
                export_data.append({
                    'streamer_data': {
                        'streamer_name': streamer.streamer_name,
                        'character_name': streamer.character_name,
                        'server': streamer.server,
                        'is_active': streamer.is_active
                    },
                    'ranking_data': {
                        'server': ranking.server,
                        'character_class': ranking.character_class,
                        'class_code': ranking.class_code or '',
                        'combat_power': ranking.combat_power
                    }
                })
        else:
            # StreamerCharacter에서 호출했을 경우 (기존 코드)
            if queryset.exists():
                streamers = queryset
                filename = f"selected_streamers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                streamers = StreamerCharacter.objects.all()
                filename = f"all_streamers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # 데이터 수집
            export_data = []
            for streamer in streamers:
                try:
                    # 랭킹 정보 가져오기
                    ranking = CharacterRanking.objects.get(streamer=streamer)
                    
                    export_data.append({
                        'streamer_data': {
                            'streamer_name': streamer.streamer_name,
                            'character_name': streamer.character_name,
                            'server': streamer.server,
                            'is_active': streamer.is_active
                        },
                        'ranking_data': {
                            'server': ranking.server,
                            'character_class': ranking.character_class,
                            'class_code': ranking.class_code or '',
                            'combat_power': ranking.combat_power
                        }
                    })
                except CharacterRanking.DoesNotExist:
                    # 랭킹 정보가 없는 경우
                    export_data.append({
                        'streamer_data': {
                            'streamer_name': streamer.streamer_name,
                            'character_name': streamer.character_name,
                            'server': streamer.server,
                            'is_active': streamer.is_active
                        },
                        'ranking_data': None
                    })
        
        # JSON 저장
        success, result = save_to_json(export_data, filename)
        
        if success:
            messages.success(request, f"{len(export_data)}개의 항목이 {filename}에 저장되었습니다.")
        else:
            messages.error(request, f"저장 오류: {result}")
    
    except Exception as e:
        messages.error(request, f"내보내기 오류: {str(e)}")
        
# 3. JSON에서 가져오기 액션
@admin.action(description="JSON 파일에서 랭킹 정보 가져오기")
def import_from_json(modeladmin, request, queryset):
    try:
        # 파일 경로 (실제 환경에 맞게 수정 필요)
        json_file = 'rankings.json'
        
        if not os.path.exists(json_file):
            messages.error(request, f"{json_file} 파일이 존재하지 않습니다.")
            return
        
        # JSON 파일 로드
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated_count = 0
        for item in data:
            try:
                streamer_data = item['streamer_data']
                ranking_data = item['ranking_data']
                
                # 스트리머 정보 업데이트 또는 생성
                streamer, created = StreamerCharacter.objects.update_or_create(
                    character_name=streamer_data['character_name'],
                    defaults={
                        'streamer_name': streamer_data['streamer_name'],
                        'server': streamer_data['server'],
                        'is_active': streamer_data['is_active']
                    }
                )
                
                # 랭킹 정보가 있는 경우에만 업데이트
                if ranking_data:
                    CharacterRanking.objects.update_or_create(
                        streamer=streamer,
                        defaults=ranking_data
                    )
                
                updated_count += 1
            except Exception as e:
                messages.warning(request, f"항목 처리 오류: {str(e)}")
                continue
        
        messages.success(request, f"{updated_count}개 항목이 성공적으로 가져와졌습니다.")
    
    except Exception as e:
        messages.error(request, f"가져오기 오류: {str(e)}")

# StreamerCharacter 관리자 설정
@admin.register(StreamerCharacter)
class StreamerCharacterAdmin(admin.ModelAdmin):
    list_display = ('streamer_name', 'character_name', 'server', 'is_active', 'created_at')
    list_filter = ('is_active', 'server')
    search_fields = ('streamer_name', 'character_name')
    actions = [export_to_json, import_from_json]  # 모든 액션 유지

# CharacterRanking 관리자 설정
@admin.register(CharacterRanking)
class CharacterRankingAdmin(admin.ModelAdmin):
    list_display = ('streamer', 'server', 'character_class', 'combat_power', 'note', 'last_updated')   
    list_editable = ('note',) 
    list_filter = ('server', 'character_class')
    search_fields = ('streamer__streamer_name', 'streamer__character_name')
    readonly_fields = ('last_updated',)
    actions = [export_to_json]  # 내보내기만 제공