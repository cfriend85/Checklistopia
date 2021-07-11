from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.create),
    path('display/<int:user_id>', views.show),
    path('display/new/item/<int:checklist_id>', views.add_item),
    path('display/delete/<int:checklist_id>', views.delete_checklist),
    path('display/delete/item/<int:items_id>', views.delete_item),
    path('display/edit/<int:checklist_id>', views.update),
    path('display/edit/update_checklist/<int:checklist_id>', views.update_checklist),
]