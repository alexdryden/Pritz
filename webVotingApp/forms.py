from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms

from webVotingApp.models import Vote, Judge, Author, Candidate, Member


# class VoteForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user')
    #
    #     super(VoteForm, self).__init__(*args, **kwargs)

    # class Meta:
    #     model = Vote
    #     fields = '__all__'
        # widgets = {
        #     'judge': CheckboxSelectMultiple,
        #     'candidate': CheckboxSelectMultiple
        # }


# class CountryForm(forms.Form):


# class NameForm(forms.Form):
#     CHOICES = (('h', 'hot', ), ('c', 'cold'), ('jr', 'just right'))
#     your_name = forms.CharField(label='Your name', max_length=100)
#     selections = forms.MultipleChoiceField(
#         choices=CHOICES,
#         widget=forms.CheckboxSelectMultiple())
    # selections = []
    # for author in Author.objects.all():
    #     selections.append(forms.BooleanField)
# _______________________________________

class MemberForm(forms.ModelForm):
    class Meta:

        model = Member
        fields = '__all__'

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()


class AuthorForm(forms.ModelForm):
    class Meta:

        model = Author
        fields = '__all__'

    def clean_first_name(self):
        return self.cleaned_data['author_first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['author_last_name'].strip()

    def clean_link(self):
        return self.cleaned_data['info_href'].strip()


class JudgeForm(forms.ModelForm):
    class Meta:

        model = Judge
        fields = '__all__'


class CandidateForm(forms.ModelForm):
    class Meta:

        model = Candidate
        fields = '__all__'


class VoteForm(forms.ModelForm):
    class Meta:

        model = Vote
        fields = '__all__'
