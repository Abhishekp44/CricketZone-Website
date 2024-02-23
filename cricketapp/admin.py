from django.contrib import admin
from cricketapp.models import Matches,Matches2,CricketNews,Teams,Players
# Register your models here.
#admin.site.register(Product)
class MatchesAdmin(admin.ModelAdmin):
    list_display=['id','name','cat','status','team1_name','team2_name', 'team1_score','team2_score','is_active']
    list_filter=['cat','is_active']

class Matches2Admin(admin.ModelAdmin):
    list_display=['id','mid','stadium','m_date','m_price']
    list_filter=['m_date','m_price']

class CricketNewsAdmin(admin.ModelAdmin):
    list_display=['id','title','ndetail','nimg']

class PlayersAdmin(admin.ModelAdmin):
    list_display=['id','tid','pname','jersey_no','cat','pimg','ptype']
    list_filter=['cat','ptype']

class TeamAdmin(admin.ModelAdmin):
    list_display=['id','tname','timage','cat']
    list_filter=['cat']

admin.site.register(Matches,MatchesAdmin)
admin.site.register(Matches2,Matches2Admin)
admin.site.register(CricketNews,CricketNewsAdmin)
admin.site.register(Players,PlayersAdmin)
admin.site.register(Teams,TeamAdmin)
