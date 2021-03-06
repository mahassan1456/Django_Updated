from tempfile import template
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice, Profile, Circle, Comments
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from polls.forms import UserSignUp, AdditionInfo, ImageForm
from django.contrib import messages
import datetime
from django.core.signals import request_finished
from PIL import Image
from django.db.models import Q
from blog.models import Article
from django.apps import apps

# Another way of getting Models from apps and helps to avoid circular imports

# Article = apps.get_model('blog','Article')




# for searching Users
class UserList(generic.ListView):
    template_name = 'polls/querylist.html'
    model = User
    context_object_name = 'search_list'

    def get_queryset(self):
        option = self.request.GET.get('option')
        query = self.request.GET.get('q')
        if option == 'User':
            q_list = User.objects.filter(Q(username__icontains = query) | Q(email__icontains = query))
            
        else:
            q_list = Question.objects.filter(Q(question_text__icontains = query) | Q(question_text__icontains = query))
            
        
        return q_list

def finished(sender, **kwargs):
    print("testing if request finished")
    print(sender)

request_finished.connect(finished)


def chart(request, question_id):
    labels =[]
    data = []
    qset = Choice.objects.filter(question= question_id)
    for dat in qset:
        labels.append(dat.choice_text)
        data.append(dat.votes)
    

    return render(request, 'polls/chart.html', {
    'labels': labels,
    'data': data,
    'question': Question.objects.get(pk=question_id).question_text
})
    

def test123(request):
    articles = Article.objects.all()
    return render(request,'admin/test123.html',context={'articles':articles})

@login_required
def index(request):
    
    latest_question_list = Question.objects.order_by('-pub_date')
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
        'Users' : User.objects.all()
    }

    return HttpResponse(template.render(context, request))

@login_required
def success(request):
    if request.method == 'POST':
        # request.FILES['picture']= request.user.profile.picture if True else ''
        form = AdditionInfo(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # request.user.profile.rs()
            
            # instance = form.save()
            # instance.user = request.user
            # instance.save()
            # # request.user.profile.bio = form.cleaned_data.get('bio')
            # # request.user.profile.location = form.cleaned_data.get('location')
            # # request.user.profile.birthdate = form.cleaned_data.get('birthdate')
            # # if form.cleaned_data.get('picture') != request.user.profile.picture:
            # #     request.user.profile.picture = form.cleaned_data.get('picture')

            # # request.user.save()
            return HttpResponseRedirect(reverse('polls:index'))
    
    # form = AdditionInfo(initial={'bio': request.user.profile.bio, 'location':request.user.profile.location,'birthdate':request.user.profile.birthdate})
    form = AdditionInfo(instance=request.user.profile)
    
    return render(request, 'polls/success.html', {'form': form})

@login_required
def make_comment(request,user_id):
    user = User.objects.get(pk=user_id)
    comment = Comments(user_c=user, comment=request.POST.get('comment'), posted_by=request.user.username)
    comment.save()

    return render(request, 'polls/view_profile.html', {'user': user})

@login_required
def view_profile(request, user_id):
    # if request.user.profile:
    #     return render(request, 'polls/view_profile.html')
    # if request.user.id != user_id:


    user = User.objects.get(pk=user_id)
    return render(request, 'polls/view_profile.html', {'user': user})
    # return HttpResponseRedirect(reverse('polls:success'))

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        url = request.GET.get('next', '')
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(url if url else reverse('polls:view_profile', args=(user.id,)))
            # # return HttpResponseRedirect(reverse('polls:success'))
            # if url:
            #     print(url)
            #     return HttpResponseRedirect(url)
            # else:
            #     print("testsuccess")
            #     print(url)
            #     return HttpResponseRedirect(reverse('polls:view_profile', args=(user.id,)))

        else:
            messages.success(request, "Username or Password is Incorrect")
            return HttpResponseRedirect(reverse('polls:login_user'))
    
    
    return render(request, 'polls/login.html', context={})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:login_user'))

def home(request):
    return render(request, 'polls/bs.html')
@login_required
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("This Question Does Not Exist")
    return render(request,'polls/details.html', context={'question': question})

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def add_friend(request, user_id):
    # usee = User.objects.get(pk=user_id)
    # print(usee)
    # friender = User.objects.get(pk=user_id)
    # friender.user.requests.add(request.user)
    # friender.save()
    # request.user.user.sent_requests.add(friender)
    # request.user.save()

    request.user.user.send_request(user_id)
    messages.success(request,f"You have sent a request to {User.objects.get(pk=user_id).username} ")
    return HttpResponseRedirect(reverse('polls:index'))
    
@login_required
def cancel_request(request, user_id):
    request.user.user.unrequest(user_id)
    return render(request, 'polls/friend_request.html')

@login_required
def accept_request(request, user_id):
    
    request.user.user.accept(user_id)
    messages.success(request, f"You are now friends with {User.objects.get(pk=user_id).username}")
    return render(request, 'polls/friend_request.html')
def remove_friend(request,user_id):
    request.user.user.remove_friend(user_id)
    messages.success(request, f"You are no longer friends with {User.objects.get(pk=user_id).username}")
    return render(request, 'polls/friend_request.html')


def vote(request,question_id):
    if request.POST.get('edit','') == 'Edit':
        
        return HttpResponseRedirect(reverse('polls:edit', args=(question_id,))) 
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': 'You did not submit a vote'
        }
        return render(request, 'polls/details.html', context)
    else:
        for item in request.user.choice_set.filter(question=choice.question):
            if choice.question == item.question:
                item.votes -= 1
                item.save()
                request.user.choice_set.remove(item)
                break
            
        choice.users.add(request.user)
        choice.save()
        choice.votes += 1
        choice.save()
        
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def sign_up(request):
    if request.method == 'POST':
        print("t----", request.POST.get('t', "non existant"))
        first = request.POST['first']
        last = request.POST['last']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            new_user = User.objects.create_user(email=email,username=email, password=password,first_name=first, last_name=last)
            new_user.save()
            return HttpResponseRedirect(reverse('polls:login_user'))
        else:
            return render(request, 'polls/sign_up.html', context= {'error_message': "Please enter the same unique password"} )
    return render(request, 'polls/sign_up.html' )

# def signup2(request):
    
#     form = UserSignUp()
#     return render(request,'polls/test.html', {'form': form})


@login_required
def add_question(request):
    if request.method == 'POST':
        
        question = request.POST.get('question','')
        if question:
            request.user.question_set.create(question_text=question, pub_date=timezone.now())
            request.user.save()
            choices = request.POST.get('choices','')
            choices_list = [x.strip() for x in choices.split('\n')]
            for x in choices_list:
                request.user.question_set.get(question_text=question).choice_set.create(choice_text=x, votes=0)
                request.user.save()
            return HttpResponseRedirect(reverse('polls:index'))

    return render(request, 'polls/add_question.html')

@login_required
def edit(request, question_id):
    question = request.user.question_set.get(pk=question_id)
    if request.method == 'POST':
        question.deleteChoices(request.POST.get('question'), request.POST.get('choices',''))
        return HttpResponseRedirect(reverse('polls:index'))



    
    return render(request, 'polls/edit.html', {'question':question})
@login_required
def profile_settings(request):
    if request.method == 'POST':
        answer = request.POST.get('answer','')
        request.user.profile.canView = answer
        request.user.save()
        return HttpResponseRedirect(reverse('polls:view_profile', args=(request.user.id,)))
    return render(request,'polls/profile_settings.html')


# def image(request):
#     if request.method == 'POST':
#         print('tttt')
#         form = ImageForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             print("valid")
#             form.save()
   
#     form = ImageForm()
#     return render(request, 'polls/images.html', {'form': form} )

def view_requests(request):
    mutuals = request.user.user.is_mutual()
    return render(request, 'polls/friend_request.html', {'mutuals': mutuals})

# @login_required
# def other_profile(request, user_id):


# def test(request):
#     if request.method == 'POST':
#         form = UserSignUp(request.POST)
#         if form.is_valid():
#             form.save()
#             print(form.cleaned_data.get('extra',''))
#             messages.success(request, "You have successfully signed up")
#         else:
#             messages.error(request, "Username already exists")

#     else:
#         form = UserSignUp()
#     return render(request, 'polls/test.html', {'form': form })
