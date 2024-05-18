from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.defaults import page_not_found
from django.contrib.auth import authenticate
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Image, Rect, Tag
from django.contrib.auth.models import User

# Create your views here.
def index(request):
	return render(request, "index.html", {})

def log(request):
	try:
		name = request.POST.get('username')
		password = request.POST.get('password')
	except KeyError:
		return HttpResponseRedirect(reverse('interface:index'))
	user = authenticate(request, username=name, password=password)
	if user == None:
		return HttpResponseRedirect(reverse('interface:index'))
	return render(request, "editor.html", {'user': user, 'image_set': user.image_set.all()})

def service(request):
	all_images = Image.objects.order_by('title')
	p = Paginator(all_images, 10)
	context = {
		'tags': Tag.objects.all(),
		'images': p.page(1).object_list,
		'site_no': 1,
		'next': 2,
		'prev': 0,
		'filtered': False
	}
	return render(request, "default.html", context)

def page(request, page_no):
	all_images = Image.objects.order_by('title')
	if len(all_images) < 10 * (page_no - 1) or page_no <= 0:
		return HttpResponse("page not found")
	if page_no == 1:
		return HttpResponseRedirect(reverse('interface:site'))
	p = Paginator(all_images, 10)
	context = {
		'tags': Tag.objects.all(),
		'images': p.page(page_no).object_list,
		'site_no': page_no,
		'next': page_no + 1,
		'prev': page_no - 1,
		'filtered': False
	}
	return render(request, "default.html", context)

def picture(request, img_id):
	image = get_object_or_404(Image, pk=img_id)
	context = {
		'image': image,
		'rect_set': image.rect_set.all()
	}
	return render(request, "picture.html", context)

def edit(request, img_id):
	user = request.POST.get('user')
	if user == None:
		return HttpResponseRedirect(reverse('interface:index'))
	image = get_object_or_404(Image, pk=img_id)
	rect_set = image.rect_set.all()
	context = {
		'user': user,
		'image': image,
		'rect_set': rect_set
	}
	return render(request, 'edit.html', context=context)

def remove_rect(request, rect_id):
	user = request.POST.get('user')
	image = request.POST.get('image')

	rect = get_object_or_404(Rect, pk = rect_id)
	image_proper = get_object_or_404(Image, title=image)

	if user != rect.image.user.username:
		return HttpResponse("remove not working")#HttpResponseRedirect(reverse('interface:index'))
	rect.delete()
	return render(request, 'edit.html', {'user': user, 'image': image_proper, 'rect_set': image_proper.rect_set.all()}) #TODO: redirect to edit

def add_rect(request):
	x, y, sizex, sizey = request.POST.get('x'), request.POST.get('y'), request.POST.get('sizex'), request.POST.get('sizey')
	image = request.POST.get('image')
	user = request.POST.get('user')
	color = request.POST.get('color')
	image_proper = get_object_or_404(Image, pk=image)
	if x == None or y == None or sizex == None or sizey == None or image == None or user == None:
		return HttpResponse("soething wrong with post")
	rect = Rect(x=x, y=y, sizex = sizex, sizey=sizey, image=image_proper, color=color)
	rect.save()
	return render(request, 'edit.html', {'user': user, 'image': image_proper, 'rect_set': image_proper.rect_set.all()})

def filter(request, page_no):
	tag_set = set()
	for tag in Tag.objects.all():
		if request.POST.get(tag.title) != None:
			tag_set.add(tag)
	sort = request.POST.get('sort')
	if len(tag_set) == 0 and sort == None:
		HttpResponseRedirect(reverse('interface:site')) #TODO: redirect to page or 404
	all_images = set()

	for tag in tag_set:
		all_images.update(tag.image_set.all())
	if len(all_images) < 10 * (page_no - 1) or page_no <= 0:
		return HttpResponse("page not found")
	
	img_list = list(all_images)
	img_list.sort(key =lambda a : a.title, reverse = (sort != None))
	p = Paginator(img_list, 10)
	
	context = {
		'tags': Tag.objects.all(),
		'filtered_tags': tag_set,
		'images': p.page(page_no).object_list,
		'site_no': page_no,
		'next': page_no + 1,
		'prev': page_no - 1,
		'sort': sort,
		'filtered': True
	}
	return render(request, "default.html", context)

def add_img(request):
	image_title = request.POST.get('image')
	username = request.POST.get('user')
	sizex = request.POST.get('sizex')
	sizey = request.POST.get('sizey')
	desc = request.POST.get('description')
	user = get_object_or_404(User, username=username)
	image, created = Image.objects.get_or_create(title=image_title, sizex=sizex, sizey=sizey, user=user, description=desc)
	if not created:
		return HttpResponse("Image already exists\n")
	image.save()
	return render(request, "editor.html", {'user': user, 'image_set': user.image_set.all()})
