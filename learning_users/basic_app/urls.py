from django.conf.urls import url
from basic_app import views

#TEMPLATE URLS!

app_name= "basic_app" # always assign the app name´s folder to the variable so I can use it in the html templates when using URL linking

urlpatterns = [
    url(r"^register/$", views.register, name="register"),
    url(r"^user_login/$", views.user_login, name="user_login"),
]