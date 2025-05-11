from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import StreamerCharacter, CharacterRanking
# from .crawler import crawl_character, crawl_all_streamers
from .crawler_playwright import crawl_all_streamers_playwright

# 관리자 확인 함수
def is_staff(user):
    return user.is_staff

def ranking_list(request):
    """랭킹 목록 보기"""
    rankings = CharacterRanking.objects.select_related('streamer').all()
    return render(request, 'tracker/ranking_list.html', {
        'rankings': rankings
    })

@login_required
@user_passes_test(is_staff)
def run_crawler(request):
    """크롤러 실행"""
    if request.method == 'POST':
        active_streamers = StreamerCharacter.objects.filter(is_active=True)
        
        if not active_streamers:
            messages.warning(request, "크롤링할 스트리머가 없습니다. 먼저 스트리머를 등록해주세요.")
            return redirect('admin:tracker_streamercharacter_add')

        results = crawl_all_streamers_playwright(active_streamers)
        updated_count = 0
        

        
        for result in results:
            if result:
                streamer = result.pop('streamer')
                CharacterRanking.objects.update_or_create(
                    streamer=streamer,
                    defaults=result
                )
                updated_count += 1
        
        messages.success(request, f"{updated_count}개의 캐릭터 정보가 업데이트되었습니다.")
        return redirect('ranking_list')
    
    return redirect('ranking_list')


