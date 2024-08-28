from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import Createuserform,userupdateform,profileupdateform
from django.contrib.auth import logout


# Create your views here.
def register(request):
    if request.method == 'POST':
       form=Createuserform(request.POST)
       if form.is_valid():
           form.save()
           return redirect('Dashboard-index')
    else:
        form=Createuserform()
    context = {
        'form':form,
    }
    return render(request,'user/register.html',context)

def userlogout(request):
    logout(request)
    # Redirect to a page after logout (optional)
    return render(request,'user/logout.html')  # Replace 'home' with the name of your desired URL pattern
def profile(request):
    return render(request,'user/profile.html')

def profile_update(request):
    
    if request.method=='POST':
        user_form = userupdateform(request.POST,instance=request.user)
        profile_form =profileupdateform(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else :
        user_form = userupdateform(instance=request.user) 
        profile_form =profileupdateform(instance=request.user.profile)  
    context={
        'user_form':user_form,
        'profile_form':profile_form,

    }
    return render(request,'user/profile_update.html',context)

