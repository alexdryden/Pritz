from django.db import models


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_last_name = models.CharField(max_length=45)
    member_first_name = models.CharField(max_length=45)

    def __str__(self):
        return '%s, %s' % (self.member_last_name, self.member_first_name)

    class Meta:
        ordering = ['member_last_name', 'member_first_name']


class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year_name = models.CharField(max_length=4)

    def __str__(self):
        return self.year_name


class Judge(models.Model):
    judge_id = models.AutoField(primary_key=True)
    year = models.ForeignKey(Year, related_name='judge', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='judge', on_delete=models.PROTECT)

    def __str__(self):
        return '%s, %s' % (self.member, self.year)


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_last_name = models.CharField(max_length=45)
    author_first_name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.author_last_name, self.author_first_name)

    class Meta:
        ordering = ['author_last_name', 'author_first_name']


class Candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, related_name='candidate', on_delete=models.CASCADE)
    year = models.ForeignKey(Year, related_name='candidate', on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.author, self.year)


class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    judge = models.ForeignKey(Judge, related_name='vote', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, related_name='vote', on_delete=models.CASCADE)

    def __str__(self):
        return '%s, %s -voted by %s' % (
            self.candidate.author.author_last_name,
            self.candidate.author.author_first_name,
            self.judge.member.member_last_name
        )


class Rating(models.Model):
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
        return (int(self.criteria_1) + int(self.criteria_2) + int(self.criteria_3) + int(self.criteria_4) + int(
            self.criteria_5)) / 5

    def __str__(self):

        def avg():
            return str((int(self.criteria_1) + int(self.criteria_2) + int(self.criteria_3) + int(self.criteria_4) + int(
                self.criteria_5)) / 5)

        return '%s, %s - Avg by %s:%s' % (
            self.candidate.author.author_last_name,
            self.candidate.author.author_first_name,
            self.judge.member.member_last_name,
            avg()
        )

