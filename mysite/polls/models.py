from datetime import datetime
from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings



# Create your models here.

# User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date Published')
    user_p = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True
    )

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def deleteChoices(self,new_question_text,choice_list):
        self.choice_set.all().delete()
        self.save()
        self.question_text = new_question_text
        self.save()
        choice_list = [x.strip() for x in choice_list.split('\n')]
        for x in choice_list:
            if x:
                self.choice_set.create(choice_text=x, votes=0)
                self.save()



    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    

    def __str__(self) -> str:
        return self.choice_text

# class Userchoice(models.Model):
#     pass


