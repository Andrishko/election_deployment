from datetime import datetime
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255)

    def __str__(self):
        return self.faculty_name


class Candidates(models.Model):
    candidate_name = models.CharField(max_length=255)
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT)
    image = models.FileField()

    def __str__(self):
        return '%s %s' % (self.candidate_name, self.faculty)


@receiver(signals.post_save, sender=Candidates)
def create_goals(sender, instance, **kwargs):
    goal = Goals(candidate_name=instance)
    goal.save()


class CustomUser(AbstractUser, PermissionsMixin):
    faculty = models.CharField(max_length=255)
    is_voted = models.BooleanField(default=False)
    token = models.CharField(max_length=1000, default='')
    time = models.CharField(
        default='2002-09-16 00:00:00', max_length=50)

    def __str__(self):
        return ""


class Goals(models.Model):
    candidate_name = models.OneToOneField(
        'Candidates', on_delete=models.CASCADE)
    candidate_goals = models.IntegerField(default=0)
    candidate_goalsno = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.candidate_goals, self.candidate_name)


class Votings(models.Model):
    start = models.DateTimeField(default=datetime.now())
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT)
    finish = models.DateTimeField(default=datetime.now())
    name = models.CharField(max_length=200, default='')
    parlament_image = models.FileField()

    def __str__(self):
        return self.name


# class VotingTime(models.Model):
#     candidate = models.CharField(max_length=255)
#     vote = models.CharField(max_length=5, default='1')
#     time = models.DateTimeField(default=timezone.now)


@receiver(signals.post_save, sender=Votings)
def create_refrained(sender, instance, **kwargs):
    refrained = Candidates(candidate_name="утримуюсь",
                           faculty=instance.faculty)
    refrained.save()
