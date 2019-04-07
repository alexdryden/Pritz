from django.contrib import admin
from .models import Member, Judge, Author, Year, Candidate, Vote, Rating

admin.site.register(Member)
admin.site.register(Judge)
admin.site.register(Author)
admin.site.register(Year)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Rating)


# Register your models here.