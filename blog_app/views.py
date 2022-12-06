from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import Blog
from django.views.generic import ListView
from django.views import View
from .forms import CommentForm
from django.urls import reverse
# Create your views here.
class StartingPage(ListView):
    model = Blog
    template_name = "blog_app/index.html"
    ordering = ["-date"]
    context_object_name = "latest_posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:2]
        return data

class AllPosts(ListView):
    model = Blog
    template_name = "blog_app/all-posts.html"
    ordering = ["date"]
    context_object_name = "posts"
    

class Post(View):
    def is_stored_post(self,request,post_id):
            stored_post = request.session.get("stored_post")
            if stored_post is not None:
                is_saved_for_later = post.id in stored_post
            else:
                is_saved_for_later = False

            return is_saved_for_later

    def get(self,request,slug):
        post = Blog.objects.get(slug=slug)
        return render(request,"blog_app/post-detail.html",context={
            "post":post,
            "tags":post.tag.all(),
            "comment_form":CommentForm,
            "comments":post.comments.all().order_by("-id"),
            "save_for_later":self.is_stored_post(request,post.id) 
        })

    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        post = Blog.objects.get(slug=slug)  
        
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog:post',args=[slug]))

        
        return render(request,"blog_app/post-detail.html",context={
            "post":post,
            "tags":post.tag.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id"),
            "save_for_later":self.is_stored_post(request,post.id) 
        })

class ReadLater(View):
    def get(self,request):
        stored_post = request.session.get("stored_post")
        context={}
        if stored_post is None or len(stored_post) ==0:
            context["posts"] = []
            context["has_posts"]=False
        else:
            posts = Blog.objects.filter(id__in=stored_post)
            context["posts"] = posts
            context["has_posts"]=True

        return render(request,"blog_app/stored_post.html",context)
    def post(self,request):
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []
        
        post_id = int(request.POST["post_id"])
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
            
            request.session["stored_post"] = stored_post
        

        return HttpResponseRedirect("/")

    
# def start_page(request):
#     latest_posts = Blog.objects.all().order_by('-date')[:2]
#     return render(request,'blog_app/index.html',context = {
#         "latest_posts":latest_posts
#     })

# def posts(request):
#     posts = Blog.objects.all().order_by('date')
#     return render(request,'blog_app/all-posts.html',context={
#         "posts":posts,
#     })


# def post(request,slug):
#     identified = get_object_or_404(Blog, slug=slug)
#     return render(request,'blog_app/post-detail.html',context={
#         "post":identified,
#         "tags":identified.tag.all(),
#         "comment_form":CommentForm()
#     })