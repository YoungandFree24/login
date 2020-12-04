from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len (postData['first_name']) < 3:
            errors['first_name'] = "first name must be at least 3 characters." 
        if len (postData['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters." 
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email"
        # test whether a field matches the pattern 
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords don't match!!!!"
        return errors

    def login_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email'] = "Invalid Email/Password"
        if len(postData['login_password']) < 8:
            errors['login'] = "Invalid Email/Password"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email= models.CharField(max_length=45)
    password= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
