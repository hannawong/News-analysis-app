'''
Models for meeting
'''
from django.db import models


class Meeting(models.Model):
    '''Meeting Model'''
    date = models.DateField('The date for meeting')
    start_time = models.CharField(max_length=30)
    position = models.CharField(max_length=100)
    teams = models.CharField(max_length=255)

    def to_dict(self):
        '''Convert Meeting into a dict'''
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'startTime': self.start_time,
            'position': self.position,
            'teams': list(filter(lambda team: team, self.teams.split('\n'))),
        }
