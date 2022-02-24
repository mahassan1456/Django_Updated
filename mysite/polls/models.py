from datetime import datetime
from distutils.command.upload import upload
from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import render



# Create your models here.

# User

class Comments(models.Model):
    user_c = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post_date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(max_length=500)
    posted_by = models.TextField(max_length=50, null=True)

    def make_comment(self, user_id):
        user = User.objects.get(pk=user_id)
        if self not in Comments.objects.all():
            user.comments_set.add(self)
            user.save()

        
        
        

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
        account = User.objects.get(pk=account)
        if account in self.requests.all():
            self.requests.remove(account)
            account.user.sent_requests.remove(self.user)
            if account not in self.friends.all():
                self.friends.add(account)
                account.user.friends.add(self.user)
                self.save()
                account.user.save()
                
    def remove_friend(self,account):
        account = User.objects.get(pk=account)
        if account in self.friends.all():
            self.friends.remove(account)
            account.user.friends.remove(self.user)
            self.save()
            account.user.save()

    def send_request(self,account):
        friender = User.objects.get(pk=account)
        if friender not in self.sent_requests.all():
            friender.user.requests.add(self.user)
            # friender.save()
            self.sent_requests.add(friender)
        # self.save()
    def is_mutual(self):
        el = []
        for friends in self.friends.all():
            for friend in friends.user.friends.all():
                if friend not in self.friends.all() and friend != self.user:
                    el.append((friends, friend))
        return el

    

    

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

@receiver(post_save, sender=Question)
def pp(sender, **kwargs):
    print('Question Created')
    for it in kwargs:
        print(it,'-',kwargs[it])
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    

    def __str__(self) -> str:
        return self.choice_text
    def make_chart(self, request, question_id):
        labels =[]
        data = []
        qset = Choice.objects.filter(question= question_id)
        for dat in qset:
            labels.append(dat.choice_text)
            data.append(dat.votes)
        print(list(zip(labels,data)))
        

        return render(request, 'polls/chart.html', {
        'labels': labels,
        'data': data,
    })


# class Userchoice(models.Model):
#     pass


