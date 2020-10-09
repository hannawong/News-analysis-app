'''
Views for meeting
'''
import datetime
import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.http import QueryDict

from .models import Meeting


def index(request):
    '''Router for meeting'''
    if request.method == 'GET':
        return get_meeting(request)
    if request.method == 'POST':
        return add_meeting(request)
    if request.method == 'DELETE':
        return delete_meeting(request)
    return HttpResponseNotAllowed(['GET', 'POST', 'DELETE'])


def get_meeting(request):
    '''GET meeting'''
    date = request.GET.get('date', '')
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest('"date" is required')
    meetings = Meeting.objects.filter(date=date)
    meetings = [meeting.to_dict() for meeting in meetings]
    return JsonResponse(meetings, safe=False)


def add_meeting(request):
    '''POST meeting'''
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return HttpResponseBadRequest()

    date = data.get('date', '')
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest('"date" is required')

    parameters = [
        ('startTime', 30),
        ('position', 100),
        ('teams', 200),
    ]
    data = {key: data.get(key) for key, _ in parameters}
    data['teams'] = '\n'.join(data['teams'])
    for parameter, limit in parameters:
        if data[parameter] is None or len(data[parameter]) > limit:
            return HttpResponseBadRequest('"%s" is required' % (parameter, ))

    meeting = Meeting(date=date,
                      start_time=data['startTime'],
                      position=data['position'],
                      teams=data['teams'])
    meeting.save()
    return HttpResponse(status=201)


def delete_meeting(request):
    '''DELETE meeting'''
    data = QueryDict(request.META['QUERY_STRING']).dict()
    print(request.META['QUERY_STRING'])
    print(data)
    try:
        meeting_id = int(data.get('id', ''))
    except ValueError:
        return HttpResponseBadRequest('"id" is required')

    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
        return HttpResponseNotFound()

    meeting.delete()
    return HttpResponse(status=202)
