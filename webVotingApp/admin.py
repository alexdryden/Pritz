from django.contrib import admin
from webVotingApp.models import  Author, Year, Candidate, Member, Judge, Vote, Rating

admin.site.register(Member)
admin.site.register(Judge)
admin.site.register(Rating)
admin.site.register(Author)
admin.site.register(Year)
admin.site.register(Candidate)



