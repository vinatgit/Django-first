from django.http import Http404
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader,RequestContext
from django.views import generic
from django.utils import timezone
from polls.forms import *

from .models import Question,Choice

class IndexView(generic.ListView):
	template_name='polls/index.html'
	context_object_name='latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(
			pub_date__lte=timezone.now()
			).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model=Question
	template_name='polls/detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request,question_id):
	question=get_object_or_404(Question,pk=question_id)
	try:
		selected_choice=question.choice_set.get(pk=request.POST['choice'])
	except(KeyError,Choice.DoesNotExist):
		return render(request,'polls/detail.html',{
			'question':question,
			'error_message':"You did not select a choice.",
		})
	else:
		selected_choice.votes+=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

class ResultsView(generic.DetailView):
	model=Question
	template_name='polls/results.html'

def register_page(request):
	if request.method=='POST':
		form=RegistrationForm(request.POST)
		if form.is_valid():
			user=User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
			return HttpResponseRedirect('/')
	form=RegistrationForm()
	variables=RequestContext(request,{'form':form})
	return render_to_response('registration/register.html',variables)
