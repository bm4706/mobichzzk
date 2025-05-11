from django.db import models

class StreamerCharacter(models.Model):
    SERVER_CHOICES = [
        ('데이안', '데이안'),
        ('아이라', '아이라'),
        ('던컨', '던컨'),
        ('알리사', '알리사'),
        ('메이븐', '메이븐'),
        ('라사', '라사'),
        ('칼릭스', '칼릭스'),
    ]
    
    streamer_name = models.CharField(max_length=50, verbose_name="스트리머 이름")
    character_name = models.CharField(max_length=50, verbose_name="캐릭터 이름")
    server = models.CharField(max_length=20, choices=SERVER_CHOICES, default='데이안', verbose_name="서버")
    is_active = models.BooleanField(default=True, verbose_name="활성 상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")
    
    def __str__(self):
        return f"{self.streamer_name} ({self.character_name}, {self.server})"
    
    class Meta:
        verbose_name = "스트리머 캐릭터"
        verbose_name_plural = "스트리머 캐릭터 목록"
        
        
class CharacterRanking(models.Model):
    streamer = models.ForeignKey(StreamerCharacter, on_delete=models.CASCADE, verbose_name="스트리머")
    server = models.CharField(max_length=20, verbose_name="서버")
    rank = models.IntegerField(null=True, blank=True, verbose_name="랭킹")
    character_class = models.CharField(max_length=20, verbose_name="클래스")    
    class_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="클래스 명명")  
    combat_power = models.IntegerField(verbose_name="전투력")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="마지막 업데이트")
    note = models.TextField(blank=True, null=True, verbose_name='비고')
    
    def __str__(self):
        return f"{self.streamer.character_name} - {self.combat_power} ({self.server})"
    
    class Meta:
        verbose_name = "캐릭터 랭킹"
        verbose_name_plural = "캐릭터 랭킹 목록"
        ordering = ['-combat_power']  # 전투력 내림차순으로 정렬