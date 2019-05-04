from django.urls import path

from webVotingApp.views import *

from . import views
urlpatterns_dict = {
                    ('member_list',''): MemberList,
                    ('judge_list', ''): JudgeList,
                    ('author_list', ''): AuthorList,
                    ('candidate_list', ''): CandidateList,
                    ('vote_list', ''): VoteList,
                    ('member_detail', '<int:pk>'): MemberDetail,
                    ('judge_detail', '<int:pk>'): JudgeDetail,
                    ('candidate_detail', '<int:pk>'): CandidateDetail,
                    ('vote_detail', '<int:pk>'): VoteDetail,
                    ('member_create', ''): MemberCreate,
                    ('judge_create', ''): JudgeCreate,
                    ('candidate_create', ''): CandidateCreate,
                    ('vote_create', ''): VoteCreate,
                    ('author_create',''): AuthorCreate,
                    ('member_update', '/<int:pk>'): MemberUpdate,
                    ('judge_update', '/<int:pk>'): JudgeUpdate,
                    ('author_update', '/<int:pk>'): AuthorUpdate,
                    ('candidate_update', '/<int:pk>'): CandidateUpdate,
                    ('vote_update', '/<int:pk>'): VoteUpdate,
                    ('member_delete', '/<int:pk>'): MemberDelete,
                    ('judge_delete', '/<int:pk>'): JudgeDelete,
                    ('candidate_delete', '/<int:pk>'): CandidateDelete,
                    ('vote_delete', '/<int:pk>'): VoteDelete,
                    ('author_delete', '/<int:pk>'): AuthorDelete,

}

urlpatterns = [path(key[0]+key[1] + '/',
                    value.as_view(),
                    name='webVotingApp_' + key[0] + '_urlpattern')
               for key, value in urlpatterns_dict.items()]

# app_name = 'webVotingApp'
# urlpatterns = [
#     path('', VotingPage.as_view, name='voting'),
#     path('authors', AuthorList.as_view, name='author_list')
# ]

# urlpatterns.append(path('vote_create/', VoteCreate.as_view(), name='webVotingApp_vote_create_urlpattern'))
# urlpatterns.append(path('vote_create2/', views.vote_create, name='webVotingApp_vote_create2_urlpattern2'))
urlpatterns.append(path('your-name/', views.get_name, name='webVotingApp_get_name_urlpattern'))
urlpatterns.append(path('thank-you/', views.thanks, name='webVotingApp_thank_you_urlpattern'))
