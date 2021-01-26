""" from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#manager for our custom model 
class MyAccountManager(BaseUserManager):
    
    #    This is a manager for Account class 
    
    def create_user(self, email, username, title, first_name, last_name, password=None):
        if not username:
            raise ValueError("Vous devez avoir un nom d'utilisateur!")
        if not email:
            raise ValueError("Vous devez avoir un email!")
        if not password:
            raise ValueError("Vous devez avoir un mot de passe!")
        if not title :
            raise ValueError("Vous devez introduire votre titre!")
        if not first_name :
            raise ValueError("Vous devez introduire votre prénom!")
        if not last_name :
            raise ValueError("Vous devez introduire votre nom!")
        user  = self.model(
                email=self.normalize_email(email),
                #password=password,
                username=username,
                title=title,
                first_name=first_name,
                last_name=last_name,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, title, first_name, last_name, password=None):
        user = self.create_user(
                email=self.normalize_email(email),
                username=username,
                title=title,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    
    
    #  Custom user class inheriting AbstractBaseUser class 
    
    
    email                = models.EmailField(verbose_name='email', max_length=60, unique=True)
    # username             = models.CharField(max_length=30, unique=True)#, default='new_user')
    date_joined          = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login           = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin             = models.BooleanField(default=False)
    is_active            = models.BooleanField(default=True)
    is_staff             = models.BooleanField(default=False)
    is_superuser         = models.BooleanField(default=False)
    title                = models.CharField(max_length=20)
    first_name           = models.CharField(max_length=50)
    last_name            = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'title', 'first_name', 'last_name',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label ):
        return True

 """
