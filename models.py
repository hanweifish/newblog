from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
# 	name = models.CharField(max_length=30)
# 	pwd = models.CharField(max_length=30)	
# 	email = models.EmailField(blank=True)


# 	def __unicode__(self):
# 		return u'%s' % self.name

class Tag(models.Model):
    tag_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
 
    def __unicode__(self):
        return self.tag_name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, blank=True)
    content = models.TextField()
    published_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
    	ordering = ['-published_time']

	def __unicode__(self):
		return u'%s %s %s' % (self.title, self.user, self.published_time)







# Create your models here.
