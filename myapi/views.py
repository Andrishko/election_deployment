import random
import string
from datetime import datetime, timedelta
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.timezone import localtime
from .models import Goals, CustomUser, Votings, Faculty
from .serializers import *
from django.db import transaction


def get_random_string(length):
    result_str = "".join(random.choice(string.ascii_letters)
                         for i in range(length))

    return result_str


def check_time(start, finish):
    return True if start < timezone.now() < finish else False


def checkvote_time(log, vote):
    return True if vote - log < timedelta(minutes=5) else False


@api_view(["POST"])
def gettokens(request: Request):
    tokens = []
    data = request.data
    i = 0
    # тут нада йобнуть bulk
    while i < int(data["number"]):
        user = CustomUser.objects.create_user(
            username=get_random_string(10), faculty=data["faculty"]
        )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        tokens.append(access_token)
        user.token = access_token
        user.save()

        i += 1

    return Response(tokens)


@api_view(["POST"])
def get_votings(request: Request):
    data = request.data
    active_votings = []

    # отримання списку голосувань
    serializer_data = Votings.objects.filter(
        Q(faculty=Faculty.objects.get(faculty_name=data["faculty"]).id)
        | Q(faculty=Faculty.objects.get(faculty_name="spu").id)
    )
    serializer = VotingsSerializer(
        instance=serializer_data, context={"request": request}, many=True
    )
    # facultys = Faculty.objects.all
    for i in serializer.data:
        start = datetime.strptime(i["start"], "%Y-%m-%dT%H:%M:%S%z")
        finish = datetime.strptime(i["finish"], "%Y-%m-%dT%H:%M:%S%z")
        if check_time(start, finish):
            # створення списку активних голосувань
            active_votings.append(
                {
                    "name": i["name"],
                    "faculty": Faculty.objects.get(id=i["faculty"]).faculty_name,
                }
            )
    return Response(active_votings)


@api_view(["GET"])
def test(request: Request, user_token):
    user = CustomUser.objects.get(token=user_token)
    vote = Votings.objects.get(
        faculty=Faculty.objects.get(faculty_name=user.faculty).id
    )
    if not check_time(vote.start, vote.finish):
        return render(request, "votingExpired.html", {"vote": vote})

    if user.is_voted == 1:
        return render(request, "youVoted.html", {"vote": vote})
    print(user.time)
    print('до перевірки')
    if user.time == '2002-09-16 00:00:00':
        user.time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        user.save()
        print(user.time)
        print('після перевірки')

    candidates = Candidates.objects.filter(
        faculty=Faculty.objects.get(faculty_name=user.faculty).id
    ).exclude(candidate_name="утримуюсь")
    abstain = Candidates.objects.get(
        faculty=Faculty.objects.get(faculty_name=user.faculty).id,
        candidate_name="утримуюсь",
    )

    context = {
        "vote": vote,
        "candidates": candidates,
        "token": user_token,
        "abstain": abstain.id,
        "time": user.time
    }

    if len(candidates) != 1:
        return render(request, "vote.html", context=context)
    return render(request, "voteSolo.html", context=context)


@api_view(["PUT"])
def votetest(request: Request):
    data = request.data
    user = CustomUser.objects.get(token=data["token"])
    candidate = Candidates.objects.get(
        candidate_name=data["candidate"],
        faculty=Faculty.objects.get(faculty_name=user.faculty).id,
    )
    vote = Votings.objects.get(faculty=candidate.faculty)
    if not check_time(vote.start, vote.finish):
        return render(request, "votingExpired.html", {"vote": vote})

    print(user.time)
    if not checkvote_time(timezone.strptime(user.time, '%Y-%m-%d %H:%M:%S'), timezone.now()):
        user.is_voted = 1
        return render(request, "thanks.html", {"vote": vote})
   
    try:
        if user.is_voted != 1:
            with transaction.atomic():
                user.is_voted = 1
                user.save()
                goals = Goals.objects.get(candidate_name=candidate.id)
                goals.candidate_goals = goals.candidate_goals + 1
                goals.save()
                votingTime = VotingTime()
                votingTime.candidate = candidate.candidate_name
                votingTime.save()
            html = render_to_string("thanks.html")
            return HttpResponse(html)
        else:
            return render(request, "youVoted.html", {"vote": vote})

    except:
        html = render_to_string("wrong.html")
        return HttpResponse(html)


@api_view(["PUT"])
def votesolo(request: Request):
    data = request.data
    user = CustomUser.objects.get(token=data["token"])
    candidate = Candidates.objects.get(
        candidate_name=data["candidate"],
        faculty=Faculty.objects.get(faculty_name=user.faculty).id,
    )
    vote = Votings.objects.get(faculty=candidate.faculty)

    if not check_time(vote.start, vote.finish):
        return render(request, "votingExpired.html", {"vote": vote})

    if not checkvote_time(user.time, timezone.now()):
        user.is_voted = 1
        return render(request, "youVoted.html", {"vote": vote})
    # аналогічно коментарю вище, засунути в транзакцію потрібно все що нище
    try:
        if user.is_voted != 1:
            with transaction.atomic():
                user.is_voted = 1
                user.save()
                goals = Goals.objects.get(candidate_name=candidate.id)
                votingTime = VotingTime()
                votingTime.candidate = candidate.candidate_name
                if data["vote"] == "yes":
                    goals.candidate_goals = goals.candidate_goals + 1
                else:
                    goals.candidate_goalsno = goals.candidate_goalsno + 1
                    votingTime.vote = '-1'
                goals.save()
                votingTime.save()
                html = render_to_string("thanks.html")
                return HttpResponse(html)
    except:
        html = render_to_string("wrong.html")
        return HttpResponse(html)
