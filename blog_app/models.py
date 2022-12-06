from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from django.urls import reverse
# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()


class Blog(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=250)
    image = models.ImageField(upload_to="images/")
    date = models.DateField(auto_now = True)
    slug =models.SlugField(blank=True,null=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="posts")
    tag = models.ManyToManyField(Tag,related_name="tags")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post", args=[self.slug])
    
    # def save(self,*args,**kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args,**kwargs)


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")

    def __str__(self):
        return self.user_name