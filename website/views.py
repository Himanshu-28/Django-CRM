from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records

# Create your views here.

def home(request):
    # Check to see if logging in
    records = Records.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']

        #Authentication

        user = authenticate(request, username = username, password = pwd)
        if user is not None:
            login(request,user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        
        else:
            messages.error(request, "There was an error logging in! Please try again.")
            return redirect('home')
        
    else:
        return render(request, 'home.html',{'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user  = authenticate(username = username, password = password)
            login (request, user)
            messages.success(request, " You have successfully registered.")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})
    
    return render(request,'register.html',{'form':form})

def update_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Records.objects.get(id=pk)
        return render(request,'record.html',{'customer_record': customer_record})
    else:
        messages.success(request,"You must be logged in to view that page!")
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Records.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Record deleted successfully.")
        return redirect('home')
    else:
        messages.success(request,"You need to be logged in to do that.")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record added.")
                return redirect('home')
        else:
            return render(request, 'add.html', {'form': form})
       
    else:
        messages.success(request,"You need to be logged in to do that.")
        return redirect('home')


