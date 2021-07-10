from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):

    def basic_validator(self, post_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}


        if len(post_data['first_name']) > 50:
            errors['first_name'] = 'Enter first name that is less than 50 characters.'
        if len(post_data['first_name']) < 1:
            errors['first_name'] = 'Enter first name that is 1 or more characters.'
        if len(post_data['last_name']) > 50:
            errors['last_name'] = 'Enter last name that is less than 50 characters.'
        if len(post_data['last_name']) < 1:
            errors['last_name'] = 'Enter last name that is 1 or more characters.'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid format for email address! (i.e. John.doe803@gmail.com)"

        try:
            User.objects.get(email = post_data['email'])
            errors['email_unique'] = 'This email is already in use.'
        except:
            pass
        
        if len(post_data['password']) < 8:
            errors['password_length'] = 'Password must be at least 8 characters.'

        if post_data['password'] != post_data['confirm']:
            
            errors['password'] = 'Password and confirm password must match.'

        return errors

class User(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 100)
    password = models.CharField(max_length= 60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()