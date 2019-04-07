from django.shortcuts import render, get_object_or_404, render_to_response
from django.views import View

from .models import (
    Judge,
    Candidate,
    Member,
    Author,
)


class VotingPage(View):
    def get(self, request):
        return render(
            request,
            'votingAppHTML/votingPage.html',
            {'author_list': Author.objects.all()}
        )


class AuthorList(View):
    def get(self, request):
        return render(
            request,
            'votingAppHTML/authorList.html',
            {'author_list': Author.objects.all()}
        )


class JudgeList(View):
    def get(self, request):
        return render(
            request,
            'votingAppHTML/memberList.html',
            {'judge_list': Judge.objects.all()}
        )


class JudgeDetail(View):
    def get(self, request, pk):
        judge = get_object_or_404(
            Judge,
            pk=pk
        )

        return render(request,
            'votingAppHTML/memberDetail.html',
            {'judge': judge}
        )


class CandidateDetail(View):
    def get(self, request, pk):
        candidate = get_object_or_404(
            Candidate,
            pk=pk
        )
        score_list = candidate.rating.all()
        avg = sum([score.avg() for score in score_list])/len(score_list)

        return render(
            request,
            'votingAppHTML/candidateDetail.html',
            {'candidate': candidate, 'score_list': score_list, 'avg': avg}
        )


class MemberDetail(View):
    def get(self, request, pk):
        member = get_object_or_404(
            Member,
            pk=pk
        )
        year_list = member.judge.all()
        return render(request,
            'votingAppHTML/memberDetail.html',
            {'member': member, 'year_list': year_list}
        )
