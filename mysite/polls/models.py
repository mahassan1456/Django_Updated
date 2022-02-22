from datetime import datetime
from distutils.command.upload import upload
from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.

# User

class Image(models.Model):
    name = models.CharField(max_length=20,null=True)
    image = models.ImageField(upload_to='test/', null=True)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True)
    picture = models.ImageField(upload_to='uploads/', null=True, verbose_name="")

class Circle(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(User, related_name='friends')
    requests = models.ManyToManyField(User, related_name='requests')
    sent_requests = models.ManyToManyField(User, related_name='sent_requests')

    def accept(self, account):
        if account in self.requests.all():
            if account not in self.friends.all():
                self.friends.add(account)
                self.save()
    def remove(self,account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
    def send_request(self,account):
        friender = User.objects.get(pk=account)
        friender.user.requests.add(self)
        friender.save()
        self.user.sent_requests.add(friender)
        self.save()

    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Circle.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
    instance.user.save()



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
        for choice in choice_list:
            if choice:
                self.choice_set.create(choice_text=choice, votes=0)
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


