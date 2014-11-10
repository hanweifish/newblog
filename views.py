from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from newblog.models import Blog, Tag
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from newblog.forms import BlogForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def blog_index(request):
	blogs = Blog.objects.all()
	return render(request, 'newblog/blog_index.html', {'blogs':blogs})


@login_required
def myblog(request):
	user = request.user
	blogs = Blog.objects.all().filter(user = user)
	return render(request, 'newblog/blog_index.html', {'blogs':blogs})


def blog_detail(request, blog_id):
	blog = get_object_or_404(Blog, pk = blog_id)
	return render(request, 'newblog/blog_detail.html', {'blog':blog})

@login_required
def blog_add(request):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data	
			title = cd['title']
			content = cd['content']
			user = request.user
			blog = Blog(title=title, user=user, content=content)
			blog.save()
			id = Blog.objects.order_by('-published_time')[0].id
			return HttpResponseRedirect('/newblog/%s' % id)
		else:
			return render(request, 'newblog/blog_add.html', {'form': form})
	else:
		form = BlogForm()
		return render(request, 'newblog/blog_add.html', {'form': form})

@login_required
def blog_update(request, blog_id=""):
	id = blog_id
	if request.method == 'POST':
		form = BlogForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			title = cd['title']
			content = cd['content']
			blog = Blog.objects.get(id=id)
			if blog:
				blog.title = title
				blog.content = content
				blog.save()
			else:
				blog = Blog(title=blog.title, content=blog.content)
				blog.save()
			return HttpResponseRedirect('/newblog/%s' % id)
	else:
		try:
			blog = Blog.objects.get(id=id)
		except Exception:
			raise Http404
		form = BlogForm(initial={'title': blog.title, 'content': blog.content}, auto_id=False)
		return render(request, 'newblog/blog_add.html', {'blog': blog, 'form': form})

@login_required
def blog_del(request, blog_id=""):
	try:
		blog = Blog.objects.get(id=blog_id)
	except Exception:
		raise Http404
	if blog:
		blog.delete()
		return HttpResponseRedirect("/newblog/myblog")
	blogs = Blog.objects.all()
	return render(request, "newblog/blog_index.html", {"blogs": blogs})




def login(request):
	if request.method == 'GET':  
		form = LoginForm()  
		return render(request, 'newblog/login.html', {'form': form})
	else:
		form = LoginForm(request.POST)  
		if form.is_valid():  
			cd = form.cleaned_data
			username = cd['username']
			password = cd['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				# return HttpResponseRedirect("newblog/")
				return HttpResponseRedirect("/newblog/myblog")
			else:
				return render(request, 'newblog/login.html', {'form': form, 'error': 'Password is wrong or the username is not existed.'})
		else:  
			return render(request, 'newblog/login.html', {'form': form, 'error': 'Username and Password is required.'})

def profile(request):
	if not request.user.is_authenticated():
		return render(request, 'newblog/login.html', {'form': form})
	return render(request, 'newblog/blog_index.html')


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/newblog/")

def signup(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)  
		if form.is_valid():
			cd = form.cleaned_data
			username = cd['username']
			password = cd['password']
			user = User.objects.create_user(username=username, password=password)
			user.save()
			user_2 = auth.authenticate(username=username, password=password)
			auth.login(request, user_2)
			# # return HttpResponseRedirect("/newblog/")
			# return render(request, 'newblog/blog_index.html')
			return HttpResponseRedirect("/newblog")
	else:
		form = LoginForm()
		return render(request, 'newblog/signup.html', {'form': form})


# Create your views here.
