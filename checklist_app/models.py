from django.db import models
from logapp.models import User
# Create your models here.
class ItemManager(models.Manager):
    
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['item_name']) < 1:
            errors['item_name'] = 'Item name is required.'
        return errors


class Item(models.Model):
    name = models.CharField(max_length=100)
    objects = ItemManager()

class ChecklistManager(models.Manager):
    
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 1:
            errors['title'] = 'Title name is required.'
        return errors

class Checklist(models.Model):
    title = models.CharField(max_length=25, default="name")
    user = models.ForeignKey(User, related_name="checklists", on_delete= models.CASCADE)
    items = models.ManyToManyField(Item, related_name="checklists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChecklistManager()