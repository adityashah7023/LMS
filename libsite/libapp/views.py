import random
from django.core import mail
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User

from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion
from django.shortcuts import get_object_or_404,render
from libapp.forms import SuggestionForm,SearchlibForm,LoginForm,ForgotPasswordForm, RegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                lucky_num=random.randint(1,9)
                request.session['lucky_num'] = lucky_num
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('libapp:index'),{'user':request.user})
            else:
                return render(request,'libapp/login.html',{'msg':'Your account is disabled.'})
        else:
            form = LoginForm()
            return render(request,'libapp/login.html',{'form':form,'msg':'Invalid login details.'})
    else:
        form=LoginForm()
        return render(request, 'libapp/login.html',{'form':form,'msg':''})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('libapp:index')))

def forgot_password(request):
    if request.method == 'POST':
        username=request.POST['username']
        if username=='':
            form = ForgotPasswordForm()
            return render(request, 'libapp/forgot.html',{'form': form, 'msg': 'Please enter username.'})
        try:
            user=User.objects.get(username=username)
            if user:
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                msg='Your password is:'+password
                mail.send_mail(
                    'Password Recovery',
                    msg,
                    '127.0.0.1',
                    [user.email],
                    fail_silently=False,
                )
                return HttpResponseRedirect(reverse('libapp:login'))
                #return render(request, 'libapp/login.html', {'form': form, 'msg': 'Please check your email.'})
                #return user_login(request)
        except User.DoesNotExist:
            form = ForgotPasswordForm()
            return render(request, 'libapp/forgot.html', {'form': form,'msg':'Invalid username. Please contact administrator.'})
    else:
        form=ForgotPasswordForm()
        return render(request, 'libapp/forgot.html', {'form':form,'msg':''})

# Create your views here.
def index(request):
    itemlist = Libitem.objects.all().order_by('title')[:10]
    return render(request, 'libapp/index.html', {'itemlist':itemlist,'user':request.user})

@login_required
def myitems(request):
    user = request.user
    if hasattr(user,'libuser'):
        booklist = Book.objects.filter(checked_out=True).filter(user__username=request.user.username)
        dvdlist = Dvd.objects.filter(checked_out=True).filter(user__username=request.user.username)
        return render(request,'libapp/myitem.html', {'booklist':booklist,'dvdlist':dvdlist,'msg':'','user':user})
    else:
        msg = "You are not a libuser."
        return render(request, 'libapp/myitem.html', {'msg': msg})

def detail(request, item_id):
    item=get_object_or_404(Libitem,id=item_id)
    response = HttpResponse()
    if item.itemtype=='Book':
        data = Book.objects.get(id=item_id)
    else :
        data = Dvd.objects.get(id=item_id)
    return render(request, 'libapp/detail.html', {'item':item,'data':data,'user':request.user})

def about(request):
    visit= int(request.COOKIES.get('about_visits','0'))
    visit = visit + 1
    max_age = 300
    response = render(request, 'libapp/about.html', {'about_visits': visit,'user':request.user})
    response.set_cookie('about_visits', visit, max_age=max_age)
    return response

def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'itemlist': suggestionlist,'user':request.user})

def suggestion(request,item_id):
    suggestion = get_object_or_404(Suggestion,id=item_id)
    return render(request, 'libapp/suggestion_details.html', {'item': suggestion,'user':request.user})

def newitem(request):
    suggestions = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect(reverse('libapp:suggestions'))
        else:
            return render(request, 'libapp/newitem.html', {'form': form, 'itemlist': suggestions, 'user':request.user})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form': form, 'itemlist': suggestions,'user':request.user})

def searchlib(request):
    if request.method == 'POST':
        form = SearchlibForm(request.POST)
        if request.POST.get("title")!='':
            booklist=Book.objects.filter(title__contains=request.POST.get("title"))
            dvdlist = Dvd.objects.filter(title__contains=request.POST.get("title"))
            if request.POST.get("by")!='':
                booklist = booklist.filter(author__contains=request.POST.get("by"))
                dvdlist = dvdlist.filter(maker__contains=request.POST.get("by"))
            return render(request, 'libapp/searchlib.html', {'form': form,'booklist':booklist,'dvdlist':dvdlist,'user':request.user})
        elif request.POST.get("by")!='':
            booklist=Book.objects.filter(author__contains=request.POST.get("by"))
            dvdlist = Dvd.objects.filter(maker__contains=request.POST.get("by"))
            return render(request, 'libapp/searchlib.html', {'form': form,'booklist':booklist,'dvdlist':dvdlist,'user':request.user})
        else:
            return render(request, 'libapp/searchlib.html', {'form': form,'user':request.user})
    else:
        form = SearchlibForm()
        return render(request, 'libapp/searchlib.html', {'form': form,'user':request.user})

def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            register.set_password(request.POST['password'])
            register.save()
            return HttpResponseRedirect(reverse('libapp:success'))
        else:
            return render(request, 'libapp/register.html', {'form': form,'user':request.user})
    else:
        form = RegisterForm()
        return render(request, 'libapp/register.html',{'form':form,'user':request.user})

def success(request):
    return render(request, 'libapp/success.html',{'user':request.user})

@login_required
def profile(request):
    user_info = User.objects.get(username=request.user.username)
    if request.method=="POST":
        form=ProfileForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
    form=ProfileForm(instance=user_info)
    return render(request, 'libapp/profile.html',{'profile':user_info,'form':form,'user':request.user})