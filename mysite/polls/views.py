from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice, Profile, Circle
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
        form = AdditionInfo(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            request.user.profile.bio = form.cleaned_data.get('bio')
            request.user.profile.location = form.cleaned_data.get('location')
            request.user.profile.birthdate = form.cleaned_data.get('birthdate')
            if form.cleaned_data.get('picture') != request.user.profile.picture:
                request.user.profile.picture = form.cleaned_data.get('picture', '')

            # pic = form.cleaned_data.get('picture')
            # print(pic)
            # print(type(pic))
            request.user.save()
            return HttpResponseRedirect(reverse('polls:index'))
    
    # form = AdditionInfo(initial={'bio': request.user.profile.bio, 'location':request.user.profile.location,'birthdate':request.user.profile.birthdate})
    form = AdditionInfo(instance=Profile.objects.get(user=request.user))
    return render(request, 'polls/success.html', {'form': form})

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
        print("post")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        url = request.GET.get('next', '')
        print("url----", url, "user----", user)
        if user is not None:
            login(request, user)
            # return HttpResponseRedirect(reverse('polls:success'))
            if url:
                print(url)
                return HttpResponseRedirect(url)
            else:
                print("testsuccess")
                print(url)
                return HttpResponseRedirect(reverse('polls:view_profile', args=(user.id,)))

        else:
            print("not logged in")
    
    
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
# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/details.html'


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'

@login_required
def add_friend(request, user_id):
    usee = User.objects.get(pk=user_id)
    print(usee)
    friender = User.objects.get(pk=user_id)
    print(friender)
    print('dddd',friender.user)
    friender.user.requests.add(request.user)
    friender.save()
    request.user.user.sent_requests.add(friender)
    request.user.save()
    # request.user.user.send_request(user_id)

    return HttpResponseRedirect(reverse('polls:index'))

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
        # question.choice_set.all().delete()
        # question.question_text = request.POST.get('question')
        # question.save()
        # choices = request.POST.get('choices','')
        # choices_list = [x.strip() for x in choices.split('\n')]
        question.deleteChoices(request.POST.get('question'), request.POST.get('choices',''))
        # for x in choices_list:
        #     question.choice_set.create(choice_text=x, votes=0)
        #     question.save()
        return HttpResponseRedirect(reverse('polls:index'))



    
    return render(request, 'polls/edit.html', {'question':question})

def image(request):
    if request.method == 'POST':
        print('tttt')
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("valid")
            form.save()
   
    form = ImageForm()
    return render(request, 'polls/images.html', {'form': form} )

def view_requests(request):

    return render(request, 'polls/friend_request.html')

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
