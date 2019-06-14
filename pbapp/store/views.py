from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


from .forms import Register, ParagraphErrorList

# Create your views here.

def index(request):
    return render(request, 'store/base.html')


def login(request):
    if request.method == 'POST':
        form = Register(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form.cleaned_data['name']
            emailUser = form.cleaned_data['email']
            passwd = form.cleaned_data['passwd']
            user = User.objects.create_user(username=name, email=emailUser, password=passwd)
            user.save()
            return HttpResponseRedirect('store/base.html')
    form = Register()
    context = {

        'form': form
    }
    return render(request, 'store/login.html', context)