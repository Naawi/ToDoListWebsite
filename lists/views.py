from django.shortcuts       import render, redirect
from django.http            import HttpResponse
from lists.models           import Item, List
from lists.forms            import ItemForm, ExistingListItemForm, NewListForm
from django.core.exceptions import ValidationError
from django.contrib.auth    import get_user_model
from html                   import unescape


User = get_user_model()

# Create your views here.
def home_page( request ):
    return render( request, 'home.html', { 'form': ItemForm() } )

def view_list( request, list_id ):
    lst = List.objects.get( id = list_id )
    form = ExistingListItemForm( for_list = lst )
    if request.method == 'POST':
        form = ExistingListItemForm( for_list = lst, data = request.POST )
        if form.is_valid():
            form.save()
            return redirect( lst )
    return render( request, 'list.html', { 'list': lst, 'form': form } )
    

def new_list( request ):
    form = NewListForm( data = request.POST )
    if form.is_valid():
        lst = form.save( owner = request.user )
        return redirect( lst )
    return render( request, 'home.html', { 'form': form } )

def my_lists(request, email):
    owner = User.objects.get( email = email )
    return render( request, 'my_lists.html', { 'owner': owner } )


