from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField 

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    
class Post(models.Model):
    
    class Status(models.TextChoices):
          DRAFT = 'DF', 'Draft'
          PUBLISHED = 'PB', 'Published'
                     
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                on_delete=models.CASCADE,
                related_name='blog_posts')
    body=RichTextUploadingField() 
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                choices=Status.choices,
                                default=Status.DRAFT)
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()
    
    class Meta:
          ordering = ['-publish']
          verbose_name_plural = "Post" 
          indexes = [
             models.Index(fields=['-publish']),
            ]
 
 
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[
                             self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
                  
class Email(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    to = models.EmailField()
    comments = models.CharField(max_length=50)

    def __str__(self):
        return self.name  
    
    class Meta:
        verbose_name_plural = "Email"  
    
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        verbose_name_plural = "Comment" 
        indexes = [
                 models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'  

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Contact"  

class About(models.Model):
    mission = models.TextField(max_length=1000)
    aboutme = models.TextField(max_length=1000)
    mission_pic = models.ImageField(upload_to='images/%Y/%m/%d/')
    aboutme_pic = models.ImageField(upload_to='images/%Y/%m/%d/')
    
    class Meta:
        verbose_name_plural = "About"
  
    
    
class OurTeam(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    profile = models.ImageField(upload_to='ourteam/%Y/%m/%d/')
    about= models.TextField(max_length=1000)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural = "OurTeam"

    
    
class Contact_details(models.Model):
    Address = models.CharField(max_length=100)
    phone_Number = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Contact_details"

                       
                        
                         