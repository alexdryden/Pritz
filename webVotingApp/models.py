from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime


#7 models
def year_validation(value):
    if value > 2100:
        raise ValidationError(
            _('%(value)s is too high to be a valid year'),
            params={'value': value}
        )
    elif value < 1900:
        raise ValidationError(
            _('%(value)s is too low to be a valid year'),
            params={'value': value}
        )


class Member(models.Model):
    def get_update_url(self):
        return reverse(
            'webVotingApp_member_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'webVotingApp_member_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_absolute_url(self):
        return reverse(
            'webVotingApp_member_detail_urlpattern',
            kwargs={'pk': self.pk}
        )
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return '%s, %s' % (self.user.last_name, self.user.first_name)
        # return self.user.last_name

    @receiver(post_save, sender=User)
    def create_user_member(sender, instance, created, **kwargs):
        if created:
            Member.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_member(sender, instance, **kwargs):
        instance.member.save()


class Year(models.Model):
    def get_update_url(self):
        return reverse(
            'webVotingApp_year_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'webVotingApp_year_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_absolute_url(self):
        return reverse(
            'webVotingApp_year_detail_urlpattern',
            kwargs={'pk': self.pk}
        )
    year_id = models.AutoField(primary_key=True)
    year_name = models.IntegerField(unique=True, validators=[year_validation], default=datetime.datetime.now().year + 1)

    def __str__(self):
        return str(self.year_name)


class Judge(models.Model):
    def get_update_url(self):
        return reverse(
            'webVotingApp_judge_update_urlpattern',
            kwargs={'pk': self.pk}
        )
    def get_delete_url(self):
        return reverse(
            'webVotingApp_judge_delete_urlpattern',
            kwargs={'pk': self.pk}
        )
    def get_absolute_url(self):
        return reverse(
            'webVotingApp_judge_detail_urlpattern',
            kwargs={'pk': self.pk}
        )
    judge_id = models.AutoField(primary_key=True)
    year = models.ForeignKey(Year, related_name='judge', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='judge', on_delete=models.PROTECT)

    def __str__(self):
        return '%s, (%i)' % (self.member, self.year.year_name)

    class Meta:
        unique_together = (('year', 'member'),)
        ordering = ['year', 'member']


class Author(models.Model):
    def get_update_url(self):
        return reverse(
            'webVotingApp_author_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'webVotingApp_author_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_absolute_url(self):
        return reverse(
            'webVotingApp_author_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    author_id = models.AutoField(primary_key=True)
    author_last_name = models.CharField(max_length=45)
    author_first_name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    info_href = models.CharField(max_length=300)

    def __str__(self):
        return '%s, %s' % (self.author_last_name, self.author_first_name)

    class Meta:
        ordering = ['author_last_name', 'author_first_name']
        unique_together = (('author_first_name', 'author_last_name'),)


class Candidate(models.Model):
    def get_update_url(self):
        return reverse(
            'webVotingApp_candidate_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'webVotingApp_candidate_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_absolute_url(self):
        return reverse(
            'webVotingApp_candidate_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    candidate_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, related_name='candidate', on_delete=models.CASCADE)
    year = models.ForeignKey(Year, related_name='candidate', on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.author, self.year)

    class Meta:
        unique_together = (('author', 'year'),)


class Vote(models.Model):
    def get_update_url(self):
        return reverse(
            'webVotingApp_vote_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'webVotingApp_vote_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_absolute_url(self):
        return reverse(
            'webVotingApp_vote_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    vote_id = models.AutoField(primary_key=True)
    judge = models.ForeignKey(Judge, related_name='vote', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, related_name='vote', on_delete=models.CASCADE)

    def __str__(self):
        return '%s, %s -voted by %s in %s' % (
            self.candidate.author.author_last_name,
            self.candidate.author.author_first_name,
            self.judge.member.user.last_name,
            self.candidate.year
        )

    class Meta:
        unique_together = (('judge', 'candidate'),)


class Rating(models.Model):

    def get_update_url(self):
        return reverse(
            'webVotingApp_rating_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'webVotingApp_rating_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_absolute_url(self):
        return reverse(
            'webVotingApp_rating_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    POOR = '1'
    COMMON = '2'
    GOOD = '3'
    OUTSTANDING = '4'
    SUPERLATIVE = '5'

    rating_choices = (
        (POOR, 'Poor'),
        (COMMON, 'Common'),
        (GOOD, 'Good'),
        (OUTSTANDING, 'Outstanding'),
        (SUPERLATIVE, 'Superlative')
    )

    rating_id = models.AutoField(primary_key=True)
    criteria_1 = models.CharField(max_length=2, choices=rating_choices)
    criteria_2 = models.CharField(max_length=2, choices=rating_choices)
    criteria_3 = models.CharField(max_length=2, choices=rating_choices)
    criteria_4 = models.CharField(max_length=2, choices=rating_choices)
    criteria_5 = models.CharField(max_length=2, choices=rating_choices)
    judge = models.ForeignKey(Judge, related_name='rating', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, related_name='rating', on_delete=models.CASCADE)

    def avg(self):
        return (int(self.criteria_1) + int(self.criteria_2) + int(self.criteria_3) + int(self.criteria_4) +
                int(self.criteria_5)) / 5

    def __str__(self):

        def avg():
            return str((int(self.criteria_1) + int(self.criteria_2) + int(self.criteria_3) + int(self.criteria_4) + int(
                self.criteria_5)) / 5)

        return '%s, %s - Avg by %s: %s' % (
            self.candidate.author.author_last_name,
            self.candidate.author.author_first_name,
            self.judge.member.user.last_name,
            avg()
        )

    class Meta:
        unique_together = (('judge', 'candidate'),)
