from django.urls import path

from webVotingApp.views import AuthorList, JudgeList, MemberDetail, CandidateDetail, VotingPage

urlpatterns_dict = {
    ('',''): VotingPage,
    ('authors',''): AuthorList,
    ('judges', ''): JudgeList,
    ('member/', '<int:pk>'): MemberDetail,
    ('candidate/', '<int:pk>'): CandidateDetail,
}

urlpatterns = [path(key[0]+key[1] + '',
                    value.as_view(),
                    name='webVotingApp' + key[0] + 'list_urlpattern')
               for key, value in urlpatterns_dict.items()]
