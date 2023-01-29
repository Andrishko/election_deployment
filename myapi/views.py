import random
import string
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

from .models import Goals, CustomUser, Votings, Faculty
from .serializers import *


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))

    return result_str


def check_time(start, finish):
    if start < timezone.now() < finish:
        return True
    else:
        return False


@api_view(['POST'])
def gettokens(request: Request):
    tokens = []
    data = request.data
    i = 0
    while i < int(data['number']):
        user = CustomUser.objects.create_user(
            username=get_random_string(10), faculty=data['faculty'])
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        tokens.append(access_token)
        user.token = access_token
        user.save()

        i += 1

    return Response(tokens)


@api_view(['POST'])
def get_votings(request: Request):
    data = request.data
    active_votings = []

    serializer_data = Votings.objects.filter(Q(faculty=Faculty.objects.get(faculty_name=data['faculty']).id) | Q(
        faculty=Faculty.objects.get(faculty_name='spu').id))  # отримання списку голосувань
    serializer = VotingsSerializer(instance=serializer_data, context={
                                   'request': request}, many=True)
    for i in serializer.data:
        if check_time(datetime.strptime(i['start'], '%Y-%m-%dT%H:%M:%S%z'),
                      datetime.strptime(i['finish'], '%Y-%m-%dT%H:%M:%S%z')):
            active_votings.append({"name": i['name'], "faculty": Faculty.objects.get(
                id=i['faculty']).faculty_name})  # створення списку активних голосувань
    return Response(active_votings)


@api_view(['GET'])
def test(request: Request, user_token):
    user = CustomUser.objects.get(
        token=user_token)
    vote = Votings.objects.get(
        faculty=Faculty.objects.get(faculty_name=user.faculty).id)

    if check_time(vote.start, vote.finish):  # time check
        if user.is_voted == 1:  # is voted check
            return render(request, 'youVoted.html', {"vote": vote})
        else:
            candidates = Candidates.objects.filter(faculty=Faculty.objects.get(
                faculty_name=user.faculty).id).exclude(candidate_name="утримуюсь")
            abstain = Candidates.objects.get(faculty=Faculty.objects.get(
                faculty_name=user.faculty).id, candidate_name="утримуюсь")

            context = {
                "vote": vote,
                "candidates": candidates,
                "token": user_token,
                "abstain": abstain.id,
            }
            print(len(candidates))
            if len(candidates) != 1:
              return render(request, 'vote.html', context=context)
            else:
              print(context['candidates'])
              return render(request, 'voteSolo.html', context=context)

    else:
        return render(request, 'votingExpired.html', {"vote": vote})


@api_view(['PUT'])
def votetest(request: Request):
    data = request.data
    vote = Votings.objects.get(
        faculty=Candidates.objects.get(id=data['candidate']).faculty)
    user = CustomUser.objects.get(token=data['token'])

    if check_time(vote.start, vote.finish):
        if user.is_voted != 1:  # is voted check
            user.is_voted = 1
            user.save()
            goals = Goals.objects.get(candidate_name=data['candidate'])
            goals.candidate_goals = goals.candidate_goals + 1
            goals.save()
        html = render_to_string('thanks.html')
        return HttpResponse(html)
    else:
        data = {
            "status": "false"
        }
        return JsonResponse(data)


@api_view(['PUT'])
def votesolo(request: Request):
    data = request.data
    vote = Votings.objects.get(
        faculty=Candidates.objects.get(id=data['candidate']).faculty)
    user = CustomUser.objects.get(token=data['token'])
    if check_time(vote.start, vote.finish):
        if user.is_voted != 1:  # is voted check
            user.is_voted = 1
            user.save()
            goals = Goals.objects.get(candidate_name=data['candidate'])
            print(data['vote'])
            if data['vote'] == 'yes':
                goals.candidate_goals = goals.candidate_goals + 1
            else:
                goals.candidate_goalsno = goals.candidate_goalsno + 1
            goals.save()
        html = render_to_string('thanks.html')
        return HttpResponse(html)
    else:
        data = {
            "status": "false"
        }
        return JsonResponse(data)
