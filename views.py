from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from newblog.models import Blog, Tag
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from newblog.forms import BlogForm, LoginForm, TagForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def blog_index(request):
	blogs = Blog.objects.all()
	tags = Tag.objects.all()
	return render(request, 'newblog/blog_index.html', {'blogs':blogs, 'tags': tags})

def blog_filter(request, id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    return render(request, "newblog/blog_filter.html",
        {"blogs": blogs, "tag": tag, "tags": tags})


@login_required
def myblog(request):
	user = request.user
	blogs = Blog.objects.all().filter(user = user)
	tags = Tag.objects.all()
	return render(request, 'newblog/blog_index.html', {'blogs':blogs, 'tags': tags})


def blog_detail(request, blog_id):
	blog = get_object_or_404(Blog, pk = blog_id)
	return render(request, 'newblog/blog_detail.html', {'blog':blog})

@login_required
def blog_add(request):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		tag = TagForm(request.POST)
		if form.is_valid() and tag.is_valid():
			cd = form.cleaned_data
			cdtag = tag.cleaned_data
			tagname = cdtag['tag_name']
			for taglist in tagname.split():
				Tag.objects.get_or_create(tag_name=taglist.strip())          
			title = cd['title']
			content = cd['content']
			user = request.user
			blog = Blog(title=title, user=user, content=content)
			blog.save()
			for taglist in tagname.split():
				blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
				blog.save()
			id = Blog.objects.order_by('-published_time')[0].id
			return HttpResponseRedirect('/newblog/%s' % id)
		else:
			return render(request, 'newblog/blog_add.html', {'form': form, 'tag':tag})
	else:
		form = BlogForm()
		tag = TagForm(initial={'tag_name': 'Notags'})
		return render(request, 'newblog/blog_add.html', {'form': form, 'tag':tag})

@login_required
def blog_update(request, blog_id=""):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		tag = TagForm(request.POST)
		if form.is_valid() and tag.is_valid():
			cd = form.cleaned_data
			cdtag = tag.cleaned_data
			tagname = cdtag['tag_name']
			tagnamelist = tagname.split()
			for taglist in tagnamelist:
				Tag.objects.get_or_create(tag_name=taglist.strip())
			title = cd['title']
			content = cd['content']
			blog = Blog.objects.get(pk=blog_id)
			user = blog.user
			if blog:
				blog.title = title
				blog.content = content
				blog.save()
				for taglist in tagnamelist:
					blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
					blog.save()
				tags = blog.tags.all()
				for tagname in tags:
					tagname = unicode(str(tagname), "utf-8")
					if tagname not in tagnamelist:
						notag = blog.tags.get(tag_name=tagname)
						blog.tags.remove(notag)
			else:
				blog = Blog(title=blog.title, content=blog.content, user=user)
				blog.save()
			return HttpResponseRedirect('/newblog/%s' % blog_id)
		else:
			return render(request, 'newblog/blog_add.html', {'form': form,'tag': tag})
	else:
		try:
			blog = Blog.objects.get(id=blog_id)
		except Exception:
			raise Http404
		form = BlogForm(initial={'title': blog.title, 'content': blog.content, 'user': blog.user}, auto_id=False)
		tags = blog.tags.all()
        if tags:
            taginit = ''
            for x in tags:
            	taginit += str(x) + ' '
            tag = TagForm(initial={'tag_name': taginit})
        else:
			tag = TagForm(initial={'tag_name': 'Notags'})
        return render(request, 'newblog/blog_add.html', {'blog': blog, 'form': form, 'blog_id': id, 'tag': tag})


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
			try:
				new_user = User.objects.create_user(username=username, password=password)
			except IntegrityError:
				error = "Username aleary existed, please choose another one"
				return render(request, 'newblog/signup.html', {'form': form, 'error':error})
			else:
				user= auth.authenticate(username=username, password=password)
				auth.login(request, user)
				return HttpResponseRedirect("/newblog")
	else:
		form = LoginForm()
		return render(request, 'newblog/signup.html', {'form': form})


# Create your views here.
