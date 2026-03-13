from django.shortcuts import render

# Create your views here.
def item_list(request):
	from .models import Item
	items = Item.objects.all()
	return render(request, 'NHM/item_list.html', {'items': items})
