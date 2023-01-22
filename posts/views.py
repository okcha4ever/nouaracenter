from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from NawaraCenter import settings
from .forms import PostForm, CommentForm
from .models import Post, Like, Comment
from django.views.generic.edit import *
from django.views.generic import TemplateView

def redirect_home(request):
    return redirect('view-home')

def home(request):
    post_list = Post.objects.all()
    posts = Post.objects.all().count()
    # get how many comments are in the post
    for post in post_list:
        post.comments_count = post.comments.count()

    return render(request, 'posts/home.html', {'post_list': post_list, 'posts': posts})

def create(request):
    perm = 0
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == 'posting':
            perm = 1


    if perm == 0:
        messages.error(request, "ليس لديك صلاحية للكتابة")
        return redirect('view-home')

    posted = False
    if request.method == 'POST':
        post = PostForm(request.POST, request.FILES)
        if post.is_valid():
            post.save()
            messages.success(request, "! تم رفع منشورك بنجاح")

        return HttpResponseRedirect('/posts/home?posted=True')
    
    else:
        initial = {'uploader': request.user.first_name + " " + request.user.last_name}
        post = PostForm(initial=initial)
        if 'posted' in request.GET:
            posted = True


    return render(request, 'posts/create.html', {'post': post, 'posted': posted})


def update(request, post_id):
    post = Post.objects.get(pk=post_id)
    initial = {'uploader': request.user.first_name + ' ' + request.user.last_name}
    form = PostForm(request.POST or None, request.FILES or None, instance=post, initial=initial)

    if form.is_valid():
        form.save()
        return redirect("view-home")

    return render(request, 'posts/update.html', {'post': post, 'form': form})

def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    messages.success(request, "تم حذف المنشور بنجاح")
    return redirect('view-home')
    
@login_required
def like(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post_obj = Post.objects.get(id=post_id)
        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)
        
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        
        like.save()

    # return redirect('view-home')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # return HttpResponseRedirect(reverse('view-home'))

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment.html'
    

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_initial(self):
        return { 'name': self.request.user.first_name + ' ' + self.request.user.last_name }

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('comments', kwargs={'pk': self.kwargs['pk']})

@login_required
def delete_comment(request, pk):
    full_name = request.user.first_name + ' ' + request.user.last_name

    comment = get_object_or_404(Comment, pk=pk)
    if comment.name == full_name:
        comment.delete()
        messages.success(request, "تم حذف التعليق بنجاح")
    else:
        messages.error(request, "ليس لديك صلاحية للحذف")

    return redirect('comments', pk=comment.post_id)

class CommentView(TemplateView):
    template_name = 'posts/comments.html'

    def get_comments(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post.comments.all().count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        context['full_name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        return context

