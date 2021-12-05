from django.db import models
from django.db.models.fields import related
import re 


#validator method
class UserValidate(models.Manager):
    def user_validator(self, data):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {} # empty dict for errors to send back
        
        if len(data['name']) < 3 or len(data['name']) > 50:
            errors['name_length error'] = "Name must be between 3 and 50 characters." #ensuring input is not too long to prevent overflow attacks
        if len(data['alias']) < 3 or len(data['alias']) > 100:
            errors['alias_length error'] = "Name must be between 3 and 100 characters."
        if not email_regex.match(data['email']):
            errors['email_format_error'] = "email must follow format example@site.com"
        if len(data['email']) > 100:
            errors['email_length_error'] = "email must be less than 100 characters long."
        if len(data['password']) > 255 or len(data['password']) < 8:
            errors['password_length_error'] = "Password must be between 8 and 255 characters long"
        # validation for passwords matching will only be done in views so no error when logging in

        return errors
    def user_login_validator(self, data):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {} # empty dict for errors to send back
        if not email_regex.match(data['email']):
            errors['email_format_error'] = "email must follow format example@site.com"
        if len(data['email']) > 100:
            errors['email_length_error'] = "email must be less than 100 characters long."
        if len(data['password']) > 255 or len(data['password']) < 8:
            errors['password_length_error'] = "Password must be between 8 and 255 characters long"
        return errors


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserValidate()


class Friendships(models.Model):
    friender = models.ForeignKey(User, related_name="the_friender", on_delete=models.CASCADE) # will be the user adding the friend
    friended_user = models.ForeignKey(User, related_name="friends", on_delete=models.CASCADE) # will be the user being added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
