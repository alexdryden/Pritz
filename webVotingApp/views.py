from collections import Counter
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
import datetime
from django.db.models import Avg, Count
from webVotingApp.models import (
    Judge,
    Candidate,
    Member,
    Author,
    Year,
    Vote,
    User,
    Rating
)
from django.core.exceptions import ObjectDoesNotExist
from .forms import JudgeForm, AuthorForm, CandidateForm, MemberForm, VoteForm, JudgeVoteForm, RatingForm


def is_member(user):
    return user.groups.filter(name='member').exists()


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
            users_name = response[1][0].split()[0]
            # users_id = request.user.id
            vote_history = Vote.objects.filter(judge__member__user_id=request.user.id)
            # user_votes = Vote.objects.filter(judge__member__user_id=request.user.id)

            if len(vote_history) > 0:
                return render(request, 'webVotingApp/already_voted.html',
                              {'vote_list': Vote.objects.all(),
                               'user_votes': vote_history})
            else:

                try:
                    year = Year.objects.get(year_name=datetime.datetime.now().year)
                except ObjectDoesNotExist:
                    year = Year.objects.create(year_name=datetime.datetime.now().year)
                    year.save()
                try:
                    member = Member.objects.get(user_id=request.user.id)
                except ObjectDoesNotExist:
                    member = Member.objects.create(user=request.user)
                    member.save()
                try:
                    judge = Judge.objects.get(year=year, member=member)
                except ObjectDoesNotExist:
                    judge = Judge.objects.create(year=year, member=member)
                    judge.save()

                for selection in response[1:]:
                    if selection[1] is int:

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
        vote_history = Vote.objects.filter(judge__member__user_id=request.user.id)
        if len(vote_history) > 0:
            dest = render(request, 'webVotingApp/already_voted.html', {
                'vote_list': Vote.objects.all(),
                'user_votes': vote_history
            })
        else:
            dest = render(request, 'webVotingApp/name.html', {'authors': Author.objects.all()})
        return dest


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
    model = Author


def thanks(request):
    return render(request, 'webVotingApp/thankyou.html', {})


def already_voted(request):
    return render(request, 'webVotingApp/already_voted.html', {})


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
                      {'member': member, 'judge_list': judge_list,
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


class AuthorDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.view_author'

    def get(self, request, pk):
        author = get_object_or_404(
            Author,
            pk=pk
        )
        candidates = author.candidate.all()
        return render(request,
                      'webVotingApp/author_detail.html',
                      {'author': author,
                       'candidates': candidates}
                      )


class VoteList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'webVotingApp.view_vote'
    model = Vote

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # pass the vote tallies of the current year
        # try:
        #     judge = Vote.objects.get(judge__member__user_id=request.user.id)
        current_year_id = Year.objects.get(year_name=datetime.datetime.now().year).year_id
        user_votes = Vote.objects.filter(judge__member__user_id=self.request.user.id)

        votes = dict(Counter([value['candidate__author__author_first_name'] +
                              ', ' +
                              value['candidate__author__author_last_name']
                              for value in list(Vote.objects.values('candidate__author__author_first_name',
                                                                    'candidate__author__author_last_name',
                                                                    'candidate__year'))
                              if value['candidate__year'] == current_year_id]))
        context['total_votes'] = votes
        context['year'] = datetime.datetime.now().year
        context['user_votes'] = user_votes
        return context


class RatingList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'webVotingApp.view_rating'
    model = Rating
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # pass the vote tallies of the current year
        # try:
        #     judge = Vote.objects.get(judge__member__user_id=request.user.id)
        current_year_id = Year.objects.get(year_name=datetime.datetime.now().year).year_id
        user_votes = Vote.objects.filter(judge__member__user_id=self.request.user.id)

        votes = dict(Counter([value['candidate__author__author_first_name'] +
                              ', ' +
                              value['candidate__author__author_last_name']
                              for value in list(Rating.objects.values('candidate__author__author_first_name',
                                                                    'candidate__author__author_last_name',
                                                                    'candidate__year'))
                              if value['candidate__year'] == current_year_id]))
        context['total_votes'] = votes
        context['year'] = datetime.datetime.now().year
        context['user_votes'] = user_votes
        return context


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


class RatingDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'webVotingApp.view_rating'

    def get(self, request, pk):
        rating = get_object_or_404(
            Rating,
            pk=pk

        )

        return render(request,
                      'webVotingApp/rating_detail.html',
                      {'rating': rating}
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

    def get_form_kwargs(self):
        kwargs = super(VoteCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    permission_required = 'webVotingApp.add_vote'
    form_class = VoteForm
    model = Vote


class RatingCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'webVotingApp.add_rating'
    form_class = RatingForm
    model = Rating


class MemberUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'webVotingApp.change_member'
    form_class = MemberForm
    model = Member
    template_name = 'webVotingApp/member_form_update.html'


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'webVotingApp.change_author'
    form_class = AuthorForm
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
    form_class = JudgeVoteForm
    model = Vote
    template_name = 'webVotingApp/vote_form_update.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # pass the vote tallies of the current year

        current_year_id = Year.objects.get(year_name=datetime.datetime.now().year).year_id
        user_votes = Vote.objects.filter(judge__member__user_id=self.request.user.id, judge__year__year_id=current_year_id)
        context['year'] = datetime.datetime.now().year
        context['user_votes'] = user_votes

        return context


class RatingUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'webVotingApp.change_rating'
    form_class = RatingForm
    model = Rating
    template_name = 'webVotingApp/rating_form_update.html'


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
        candidates = author.candidate.all()
        if candidates.count() > 0:
            return render(
                request,
                'webVotingApp/author_refuse_delete.html',
                {'author': author,
                 'candidates': candidates}
            )
        else:
            return render(
                request,
                'webVotingApp/author_confirm_delete.html',
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


class RatingDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'webVotingApp.delete_rating'
    model = Rating
    success_url = reverse_lazy('webVotingApp_rating_list_urlpattern')
