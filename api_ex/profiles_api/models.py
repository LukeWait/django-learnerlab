from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class  UserProfileManager(BaseUserManager):
    """Manager for user profile """

    def create_user(self,email, name, password=None):
        if not email:
            raise ValueError('user must have an emails')
        
        email = self.normalize_email(email) # set to lower case after @
        user = self.model(email=email, name=name)

        user.set_password(password) # hash the password
        user.save(using=self._db)

        return user 


    def create_super(self, email, name, password):
        """Create a Admin Account"""
        user = self.create_user((email, name, password)) # using our own creat_user

        user.is_superuser = True # turn on admin flag
        user.is_staff = True # add user to staff group

        return user 


# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model user in the system - overwritting the the standard user"""
    email = models.EmailField(max_length=255, unique=True)
    name=models.CharField(max_length=255)
    is_active  = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects= UserProfileManager() # django admin to use to create the user 

    USERNAME_FIELD = 'email' # this the new uaername
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Get full name of user"""
        return self.name

    def get_short_name(self):
        """Get full name of user"""
        return self.name

    def __str__(self):
        return self.email
