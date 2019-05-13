from django.urls import path

from webVotingApp.views import *

from webVotingApp import views


urlpatterns_dict = {
                    ('member_list',''): MemberList,
                    ('judge_list', ''): JudgeList,
                    ('author_list', ''): AuthorList,
                    ('candidate_list', ''): CandidateList,
                    ('vote_list', ''): VoteList,
                    ('rating_list', ''): RatingList,
                    ('member_detail', '<int:pk>'): MemberDetail,
                    ('judge_detail', '<int:pk>'): JudgeDetail,
                    ('candidate_detail', '<int:pk>'): CandidateDetail,
                    ('author_detail', '<int:pk>'): AuthorDetail,
                    ('vote_detail', '<int:pk>'): VoteDetail,
                    ('rating_detail', '<int:pk>'): RatingDetail,
                    ('member_create', ''): MemberCreate,
                    ('judge_create', ''): JudgeCreate,
                    ('candidate_create', ''): CandidateCreate,
                    ('vote_create', ''): VoteCreate,
                    ('author_create',''): AuthorCreate,
                    ('rating_create', ''): RatingCreate,
                    ('member_update', '/<int:pk>'): MemberUpdate,
                    ('judge_update', '/<int:pk>'): JudgeUpdate,
                    ('author_update', '/<int:pk>'): AuthorUpdate,
                    ('candidate_update', '/<int:pk>'): CandidateUpdate,
                    ('vote_update', '/<int:pk>'): VoteUpdate,
                    ('rating_update','/<int:pk>'): RatingUpdate,
                    ('member_delete', '/<int:pk>'): MemberDelete,
                    ('judge_delete', '/<int:pk>'): JudgeDelete,
                    ('candidate_delete', '/<int:pk>'): CandidateDelete,
                    ('vote_delete', '/<int:pk>'): VoteDelete,
                    ('author_delete', '/<int:pk>'): AuthorDelete,
                    ('rating_delete', '/<int:pk>'): RatingDelete


}

urlpatterns = [path(key[0]+key[1] + '/',
                    value.as_view(),
                    name='webVotingApp_' + key[0] + '_urlpattern')
               for key, value in urlpatterns_dict.items()]

urlpatterns.append(path('first-round-vote/', views.get_name, name='webVotingApp_get_name_urlpattern'))
urlpatterns.append(path('thank-you/', views.thanks, name='webVotingApp_thank_you_urlpattern'))
urlpatterns.append(path('vote-recorded/', views.already_voted, name='webVotingApp_already_voted_urlpattern'))

