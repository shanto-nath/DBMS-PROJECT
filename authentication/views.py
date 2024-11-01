from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, SignInForm, EditProfileForm
from .models import UserProfile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import os

# Create your views here.
    
def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, "You have already Signed In")
        return redirect('/')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            nid = form.cleaned_data['nid']
            user_type = form.cleaned_data['user_type']



            user = User.objects.create_user(username=email, email = email, password = password)

            user_profile = UserProfile.objects.create(name = name.capitalize(), email = email, nid = nid, user_type=user_type)
            user_profile.user = user
            user_profile.save()

            messages.success(request, "Registration successful. Please sign in.")
            return redirect('signin')
        
    
    else:
        form = SignUpForm()

    return render(request, "signup.html", {'form': form})


def signin(request):
    if request.user.is_authenticated:
        messages.warning(request, "You have already Signed In")
        return redirect('/')
    
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session['isLoggedIn'] = True
                messages.success(request, "Successfully Signed in")
                next_url = request.GET.get('next')
                if next_url:
                    if(next_url == "/authentication/signup" or next_url == "/authentication/signin"):
                        return redirect("/")
                    else:
                        return redirect(next_url)
                else:
                    return redirect("/")
    
    else:        
        form = SignInForm()
    
    return render(request, "signin.html", {'form': form})

@login_required
def signout(request):
    logout(request)
    request.session['isLoggedIn'] = False
    next_page = request.GET.get('next', '/')
    messages.success(request, "Successfully Signed Out")
    return redirect(next_page)


def profile(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user = request.user)
        profile_fields = get_profile_fields(user_profile)
        profile_fields['profile_picture'] = user_profile.profile_picture
        return render(request, "profile.html", {'profile_fields':profile_fields})
    else:
        return redirect(reverse('signin') + '?next=' + request.path)


def get_profile_fields(user_profile):
    fields = [field.name for field in UserProfile._meta.get_fields() if field.name in ['name', 'email', 'contact_no', 'gender', 'nid', 'dob', 'address', 'user_type']]
    return {field: getattr(user_profile, field, None) for field in fields}


def edit_profile(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user = request.user)

        if request.method == 'POST':    
            form = EditProfileForm(request.POST, request.FILES, instance = user_profile)
            if form.is_valid():
                request.user.email = form.cleaned_data['email']
                request.user.username = form.cleaned_data['email']
                request.user.save()

                form.save()
                return redirect('profile')
            
        else:
            form = EditProfileForm(instance=user_profile)

        return render(request, 'edit_profile.html', {'form':form})
    
    else:
        return redirect(reverse('signin') + '?next=' + request.path)

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            user.delete()
            logout(request)
            messages.success(request, "Account deleted successfully")
            return redirect('/')
        else:
            messages.error(request, "Invalid password. Account deletion failed.")
            return redirect('profile')
    else:
        return redirect('profile')
