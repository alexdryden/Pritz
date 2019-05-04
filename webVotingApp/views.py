from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from webVotingApp.models import Vote
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
import datetime
from .models import (
    Judge,
    Candidate,
    Member,
    Author,
    Year
)
from django.core.exceptions import ObjectDoesNotExist
from .forms import JudgeForm, AuthorForm, CandidateForm, MemberForm, VoteForm
from collections import Counter


def get_name(request):
    if request.method == 'POST':
        candidate_ids = [checkbox[1] for checkbox in list(request.POST.items())[1:]]
        valid = True
        # for candidate_id in candidate_ids:
        #     try:
        #         Candidate.objects.get(candidate_id=candidate_id)
        #     except ObjectDoesNotExist:
        #         valid = False

        if valid:
            response = list(request.POST.items())
            user = response[1][0].split()
            try:
                year = Year.objects.get(year_name=datetime.datetime.now().year)
            except ObjectDoesNotExist:
                year = Year.objects.create(year_name=datetime.datetime.now().year)
                year.save()
            try:
                member = Member.objects.get(member_first_name=user[0], member_last_name=user[1])
            except ObjectDoesNotExist:
                member = Member.objects.create(member_first_name=user[0], member_last_name=user[1])
                member.save()
            try:
                judge = Judge.objects.get(year=year, member=member)
            except ObjectDoesNotExist:
                judge = Judge.objects.create(year=year, member=member)
                judge.save()

            for selection in response[1:]:
                author = Author.objects.get(author_id=selection[1])
                try:
                    candidate = Candidate.objects.get(author=author, year=year)
                except ObjectDoesNotExist:
                    candidate = Candidate.objects.create(author=author, year=year)
                    candidate.save()
                vote = Vote.objects.create(candidate=candidate, judge=judge)
                vote.save()

            return HttpResponseRedirect(reverse('webVotingApp_thank_you_urlpattern'))
    else:
        return render(request, 'webVotingApp/name.html', { 'authors': Author.objects.all()})


# class VotingPage(View):
#     def get(self, request):
#         return render(
#             request,
#             './webVotingApp/votingPage.html',
#             {'author_list': Author.objects.all()}
#         )
# 
# 
class AuthorList(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'webVotingApp.view_author'
    # def get(self, request):
    #     return render(
    #         request,
    #         './webVotingApp/author_list.html',
    #         {'author_list': Author.objects.all()}
    #     )
    model = Author
# 
# 
# class JudgeList(ListView):
#     # def get(self, request):
#     #     return render(
#     #         request,
#     #         './webVotingApp/judge_list.html',
#     #         {'judge_list': Judge.objects.all()}
#     #     )
#     model = Judge
# 
# 
# class JudgeDetail(View):
#     def get(self, request, pk):
#         judge = get_object_or_404(
#             Judge,
#             pk=pk
#         )
# 
#         return render(request,
#                       './webVotingApp/memberDetail.html',
#                       {'judge': judge}
#                       )
# 
#


# class CandidateDetail(View):
#     def get(self, request, pk):
#         candidate = get_object_or_404(
#             Candidate,
#             pk=pk
#         )
#         score_list = candidate.rating.all()
#         avg = sum([score.avg() for score in score_list])/len(score_list)
#
#         return render(
#             request,
#             './webVotingApp/old_templates/candidateDetail.html',
#             {'candidate': candidate, 'score_list': score_list, 'avg': avg}
#         )
# 
# 
# class MemberDetail(View):
#     def get(self, request, pk):
#         member = get_object_or_404(
#             Member,
#             pk=pk
#         )
#         year_list = member.judge.all()
#         return render(request,
#                       './webVotingApp/memberDetail.html',
#                       {'member': member, 'year_list': year_list}
#                       )


def thanks(request):

    return render(request, 'webVotingApp/thankyou.html', {})

#___________________________________________________________


class MemberList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'webVotingApp.view_member'
    model = Member


class MemberDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.view_member'

    def get(self, request, pk):
        member = get_object_or_404(
            Member,
            pk=pk

        )
        judge_list = member.judge.all()
        return render(request,
                      'webVotingApp/member_detail.html',
                      {
                'member': member,
                'judge_list': judge_list,
            }
                      )


class JudgeList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'webVotingApp.view_judge'
    model = Judge


class JudgeDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.view_judge'

    def get(self, request, pk):
        judge = get_object_or_404(
            Judge,
            pk=pk
        )
        member = judge.member
        vote_list = judge.vote.all()
        return render(request,
                      'webVotingApp/judge_detail.html',
                      {
                'judge': judge,
                'member': member,
                'vote_list': vote_list,

            }

                      )


class CandidateList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'webVotingApp.view_candidate'
    model = Candidate


class CandidateDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.view_candidate'

    def get(self, request, pk):
        candidate = get_object_or_404(
            Candidate,
            pk=pk

        )
        vote_list = candidate.vote.all()
        return render(request,
                      'webVotingApp/candidate_detail.html',
                      {'candidate': candidate,
                       'vote_list': vote_list,}
                      )


class VoteList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'webVotingApp.view_vote'
    model = Vote


# class VoteList(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = 'webVotingApp.view_vote'
#     def get(self, request):
#         votes = Vote.objects.only('candidate')
#         counts = Counter(votes)
#         return render(request, 'webVotingApp/vote_list.html', {'counts': counts})

    # model = Vote
# class VoteList(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = 'webVotingApp.view_vote'
#     def get(self, request):
#         votes = Vote.objects.only('candidate')
#         for vote in votes:
#             vote.candidate

    # model = Vote for ListView

# class CandidateDetail(View):
#     def get(self, request, pk):
#         candidate = get_object_or_404(
#             Candidate,
#             pk=pk
#         )
#         score_list = candidate.rating.all()
#         avg = sum([score.avg() for score in score_list])/len(score_list)
#
#         return render(
#             request,
#             './webVotingApp/old_templates/candidateDetail.html',
#             {'candidate': candidate, 'score_list': score_list, 'avg': avg}
#         )

class VoteDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.view_vote'

    def get(self, request, pk):
        vote = get_object_or_404(
            Vote,
            pk=pk

        )

        return render(request,
                      'webVotingApp/vote_detail.html',
                      {'vote': vote}
                      )


class MemberCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'webVotingApp.add_member'
    form_class = MemberForm
    model = Member


class JudgeCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'webVotingApp.add_judge'
    form_class = JudgeForm
    model = Judge


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'webVotingApp.add_author'
    form_class = AuthorForm
    model = Author


class CandidateCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'webVotingApp.add_candidate'
    form_class = CandidateForm
    model = Candidate


class VoteCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'webVotingApp.add_vote'
    form_class = VoteForm
    model = Vote


class MemberUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'webVotingApp.change_member'
    form_class = MemberForm
    model = Member
    template_name = 'webVotingApp/member_form_update.html'


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'webVotingApp.change_author'
    form_class = MemberForm
    model = Author
    template_name = 'webVotingApp/author_form_update.html'


class JudgeUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'webVotingApp.change_judge'
    form_class = JudgeForm
    model = Judge
    template_name = 'webVotingApp/judge_form_update.html'



class CandidateUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'webVotingApp.change_candidate'
    form_class = CandidateForm
    model = Candidate
    template_name = 'webVotingApp/candidate_form_update.html'


class VoteUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'webVotingApp.change_vote'
    form_class = VoteForm
    model = Vote
    template_name = 'webVotingApp/vote_form_update.html'


class MemberDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.delete_member'

    def get(self, request, pk):
        member = self.get_object(pk)
        judges = member.judge.all()
        if judges.count() > 0:
            return render(
                request,
                'webVotingApp/member_refuse_delete.html',
                {'member': member,
                 'judges': judges}
            )
        else:
            return render(
                request,
                'webVotingApp/member_confirm_delete.html',
                {'member': member}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Member,
            pk=pk
        )

    def post(self, request, pk):
        member = self.get_object(pk)
        member.delete()
        return redirect('webVotingApp_member_list_urlpattern')


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.delete_author'

    def get(self, request, pk):
        author = self.get_object(pk)
        candidate = author.candidate.all()
        if candidate.count() > 0:
            return render(
                request,
                'webVotingApp/member_refuse_delete.html',
                {'author': author,
                 'candidate': candidate}
            )
        else:
            return render(
                request,
                'webVotingApp/member_confirm_delete.html',
                {'author': author}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Author,
            pk=pk
        )

    def post(self, request, pk):
        author = self.get_object(pk)
        author.delete()
        return redirect('webVotingApp_author_list_urlpattern')


class JudgeDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.delete_judge'

    def get(self, request, pk):
        judge = self.get_object(pk)
        votes = judge.vote.all()
        if votes.count() > 0:
            return render(
                request,
                'webVotingApp/judge_refuse_delete.html',
                {'judge': judge,
                 'votes': votes}
            )

        else:
            return render(
                request,
                'webVotingApp/judge_confirm_delete.html',
                {'judge': judge}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Judge,
            pk=pk
        )

    def post(self, request, pk):
        judge = self.get_object(pk)
        judge.delete()
        return redirect('webVotingApp_judge_list_urlpattern')



class CandidateDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.delete_candidate'

    def get(self, request, pk):
        candidate = self.get_object(pk)
        votes = candidate.vote.all()
        if votes.count() > 0:
            return render(
                request,
                'webVotingApp/candidate_refuse_delete.html',
                {'candidate': candidate,
                 'votes': votes}
            )
        else:
            return render(
                request,
                'webVotingApp/candidate_confirm_delete.html',
                {'candidate': candidate}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Candidate,
            pk=pk
        )

    def post(self, request, pk):
        candidate = self.get_object(pk)
        candidate.delete()
        return redirect('webVotingApp_candidate_list_urlpattern')


class VoteDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'webVotingApp.delete_vote'
    model = Vote
    success_url = reverse_lazy('webVotingApp_vote_list_urlpattern')
