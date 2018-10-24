from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    if 'id' in request.session:
        return redirect('/wall')

    return render(request, 'wall/index.html')

def register(request):
    if request.method != 'POST':
        return redirect('/')

    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    else:
        user = User.objects.create_user(request.POST)
        request.session['id'] = user.id
        messages.success(request, "Successfully Registered!")
        return redirect('/wall')

def wall(request):
    if 'id' not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['id']),
        'post_data': Message.objects.all(),
        'comment_data': Comment.objects.all()
    }

    return render(request, 'wall/wall.html', context)

def login(request):
    if request.method != 'POST':
        return redirect('/')

    valid, response = User.objects.login(request.POST)
    if valid == True:
        request.session['id'] = response
        messages.success(request, "Successfully logged in.")
        return redirect('/wall')
    else:
        messages.error(request, response)

    return redirect('/')

    # email = request.POST['email']
    # password = request.POST['password']

    # user = User.objects.filter(email=email)
    # if len(user) > 0:
    #     if bcrypt.checkpw(password.encode(), user[0].password.encode()):
    #         request.session['id'] = user[0].id
    #         messages.success(request, "Successfully logged in.")
    #         return redirect('/wall')
    #     else:
    #         messages.error(request, "Incorrect email/password combination.")
    #         return redirect('/')

    # else:
    #     messages.error(request, "Account does not exist.")
    #     return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_message(request):
    Message.objects.create(message=request.POST['add_message'], user=User.objects.get(id=request.session['id']))
    messages.success(request, "Message posted successfully.")
    return redirect('/wall')

def delete_message(request, id):
    Message.objects.get(id=id).delete()
    return redirect('/wall')

def comment(request):
    Comment.objects.create(comment=request.POST['comment'], user=User.objects.get(id=request.session['id']), message=Message.objects.get(id=request.POST['message_ID']))
    return redirect('/wall')