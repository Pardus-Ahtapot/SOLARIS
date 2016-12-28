from django.shortcuts import render
from django.template.context_processors import csrf
from django.shortcuts import render_to_response

from django.contrib import auth
from django.http import HttpResponseRedirect


def home(request):

    return render(request, 'home.html')


def login(request):
    context={}
    context.update(csrf(request))
    if request.GET:
        context['next'] = request.GET['next']
    else:
        context['next'] = "/"
    return render_to_response('login.html', context)


def authenticate(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request, user)
        redir = request.POST["next"]
        return HttpResponseRedirect(redir)
    else:
        return HttpResponseRedirect('/auth/login')


def logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/auth/login/')
    username = request.user.username
    auth.logout(request)
    return HttpResponseRedirect('/')
