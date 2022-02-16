from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone



@login_required
def index(request):
    
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }

    return HttpResponse(template.render(context, request))

@login_required
def success(request):
    print(request.user)
    return render(request, 'polls/success.html')


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
                return HttpResponseRedirect(reverse('polls:success'))

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
def vote(request,question_id):
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
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def sign_up(request):
    if request.method == 'POST':
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
            return HttpResponseRedirect(reverse('polls:index'))

    return render(request, 'polls/add_question.html')
