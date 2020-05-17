from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# for login:
from django.urls import reverse
# Note! before it was another library (course) but django 3 changed it, so now import from django.urls library!!
from django.contrib.auth.decorators import login_required
# whenever I want a view where a user is required to login, I can use this decorator to block the view
#django has several auth decorators!
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def index(request):
    return render(request, "basic_app/index.html")


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST) # this matches the variable we are going to send back with the context dictionary
        profile_form = UserProfileInfoForm(data=request.POST)

        #check if both forms are valid:
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password) # set_password method means we are hashing the password -> goes into setting. py file and there it will be hashed
            user.save()

            profile = profile_form.save(commit=False) # we don t want to send it to the database yet, otherwise we may get error with collissions where it tries to override the user variable
            profile.user = user # with this code we set the code from models.py: user = models.OneToOneField, means now the user profile belongs to user , no errors
            # means the profile belongs to this one specific user

            if "profile_pic" in request.FILES: #checking if the user added a profile pic, important: always: FILES!! not Files!
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm() # need the brackets?
        profile_form = UserProfileInfoForm

    return render(request, "basic_app/registration.html", {"user_form":user_form, "profile_form":profile_form, "registered":registered})

# superuser: username: manu, pw: manumanu12, mail: manu@gmail.com

@login_required # we only want to log out someone who logged in before, so we call this decorator who checks for this condition
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index")) # after logout will be redirected to index homepage

@login_required # this function will asign the logged in person to a page which only logged in people can see, so the decorator needs to check
def special(request):
    return HttpResponse("You are now logged in!")


def user_login(request): #note! in future never name a function same as an import function as it might get overwritten and return errors

    if request.method == "POST":
        #step one - get username and password supplied:
        username = request.POST.get("username") # in our login html we defined that input for username has the name: username, as we want top grab the data of this we grab the name of this tag
        password = request.POST.get("password")

        user=authenticate(username=username, password=password) # sometimes django complains if I simply do: (username, password) so better do username= username etc.
        #this line will automatically authenticate the user for me, means, check if the password and username are correct and which user it is

        if user:
            if user.is_active: # means if the user is still in databse and not deactived for some reasons
                login(request, user) # we log the user in
                return HttpResponseRedirect(reverse("index")) # we use http response... to redirect the user, in this case we send him back to the homepage (index)

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE!")

        else:
            print("Someone tried to login and failed")
            print(f"Username: {username} and password: {password}")
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request, "basic_app/login.html", {}) #{} is not mandatory