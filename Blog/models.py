
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null =True, blank = True)
    tag = models.ManyToManyField(Tag, blank= True)
    
    def __str__(self):
        return self.title
 

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE) 
    commenter=models.CharField(max_length=100)
    
    def __str__(self):
        return self.commenter

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}-{self.post}"