from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,get_user_model,login,logout
from .forms import UserLoginForm,UserRegistrationForm

def login_view (request):
    form = UserLoginForm(request.POST or None)
    titel = "Login"
    next=request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username,password=password)
        login(request,user)

        if next:
            return redirect(next)
        return redirect("/")
    template_name = 'login.html'
    context = {
        "titel": titel,
        "form": form

    }
    return render(request,template_name,context)

def regstration_view (request):
    form = UserRegistrationForm(request.POST or None)
    titel = "Registration Form"
    next = request.GET.get('next')

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        if next:
            return redirect(next)
        return redirect("/login/")
    template_name = 'registration.html'
    context = {
        "titel": titel,
        "form": form

    }
    return render(request,template_name,context)

def logout_view (request):
    logout(request)
    return redirect("/login/")