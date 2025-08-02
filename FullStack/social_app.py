# social_app_combined.py
# Includes models, views, urls, and templates as string (for quick testing)

# MODELS (main/models.py)
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# VIEWS (main/views.py)
from django.shortcuts import render, redirect
# from .models import Post, Comment, Follow
# Models are defined above in this file, so we can use them directly.
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})

@login_required
def profile(request):
    user_posts = Post.objects.filter(user=request.user)
    return render(request, 'profile.html', {'posts': user_posts})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post, user=request.user, content=request.POST['content'])
    return redirect('index')

@login_required
def follow_user(request, user_id):
    followed_user = User.objects.get(id=user_id)
    Follow.objects.get_or_create(follower=request.user, followed=followed_user)
    return redirect('index')


# TEMPLATE: index.html
"""
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head><title>Feed</title></head>
<body>
    <h1>Social Media Feed</h1>
    {% for post in posts %}
        <div>
            <h3>{{ post.user.username }}</h3>
            <p>{{ post.content }}</p>
            <form method="POST" action="{% url 'add_comment' post.id %}">
                {% csrf_token %}
                <input type="text" name="content" placeholder="Write a comment...">
                <button type="submit">Comment</button>
            </form>
        </div>
        <hr>
    {% endfor %}
</body>
</html>
"""

# TEMPLATE: profile.html
"""
<!-- templates/profile.html -->
<!DOCTYPE html>
<html>
<head><title>Profile</title></head>
<body>
    <h1>Your Posts</h1>
    {% for post in posts %}
        <div>
            <p>{{ post.content }}</p>
        </div>
        <hr>
    {% endfor %}
</body>
</html>
"""

# CSS (static/styles.css)
"""
body {
    font-family: Arial, sans-serif;
    padding: 20px;
}
input[type="text"] {
    width: 300px;
    padding: 5px;
}
"""