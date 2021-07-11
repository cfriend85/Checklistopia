from django.shortcuts import redirect, render, HttpResponse
from logapp.models import User
from django.contrib import messages
from .models import Item, Checklist

# Shows the main page after login with form to create checklist
def index(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'dashboard.html', context)


# Processes the form to create a new checklist
def create(request):
    errors = Checklist.objects.basic_validator(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
            return redirect('/checklist')

    Checklist.objects.create(
        title = request.POST['title'],
        user = User.objects.get(id=request.session['user_id'])
    )
    return redirect(f"display/{request.session['user_id']}")


# Shows the user thier page with all of thier checklists on it as well as form to add items to a checklist
def show(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'checklists': Checklist.objects.filter(user_id=user_id),
    }
    return render(request, 'show.html', context)


# Processes the form to add items to a checklist
def add_item(request, checklist_id):
    errors = Item.objects.basic_validator(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f"/checklist/display/{request.session['user_id']}")
    
    item = Item.objects.create(
        name = request.POST['item_name'],
    )
    this_checklist = Checklist.objects.get(id=checklist_id)
    this_item = Item.objects.get(id=item.id)
    this_checklist.items.add(this_item)

    return redirect(f"/checklist/display/{request.session['user_id']}")


# Deletes checklist
def delete_checklist(request, checklist_id):
    checklist = Checklist.objects.get(id=checklist_id)
    checklist.delete()

    return redirect('/checklist')

# Delete indiviual item from a checklist
def delete_item(request, items_id):
    item = Item.objects.get(id= items_id)
    item.delete()

    return redirect(f"/checklist/display/{request.session['user_id']}")

# Shows form to update checklist title
def update(request, checklist_id):
    context = {
        'checklist': Checklist.objects.get(id=checklist_id)
    }
    return render(request, 'checklist.html', context)

# Process form data
def update_checklist(request, checklist_id):
    errors = Checklist.objects.basic_validator(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f"/checklist/display/edit/{checklist_id}")

    checklist = Checklist.objects.get(id=checklist_id)
    checklist.title = request.POST['title']
    checklist.save()

    return redirect(f"/checklist/display/{request.session['user_id']}")