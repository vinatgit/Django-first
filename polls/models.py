from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Question(models.Model):
    def __str__(self):
        return self.question_text
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    
    def was_published_recently(self):
    	return timezone.now()-datetime.timedelta(days=1)<=self.pub_date<=timezone.now()
    was_published_recently.admin_order_field='pub_date'
    was_published_recently.boolean=True
    was_published_recently.short_description='Published recently?'

class Choice(models.Model):
    def __str__(self):
        return self.choice_text
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

class Voter(models.Model):
    question=models.ForeignKey(Question)
    user=models.ForeignKey(User)
#Create your models here.
