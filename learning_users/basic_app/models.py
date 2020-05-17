from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model): # never inherit directly form User as this might screw up the database

    user = models.OneToOneField(User, on_delete=models.CASCADE) # as this class already has a lot of attributes and we want only to add soe new but not ignore the others
    #we take one t one field, means it sdirectly what is in the other class
    # we assign it to user so we could exclue it in our forms class so that we only show some new created forms which we created in this class

    #additional attributes:
    portfolio_site = models.URLField(blank=True) # blank, true means that it s optional so user doesn t have to fill it out

    profile_pic = models.ImageField(upload_to="profile_pics", blank=True) # we need to specify, where it has to be uploaded to, + it s optional user doesn t have to upload
    # upload to, profile pics: we create the folder profile_pics (as we named it that way) inside of the media folder
    # so user pics -> will be saved in the profile_pics folder!

    def __str__(self):
        return self.user.username # username is a default attribute of User class, we imported