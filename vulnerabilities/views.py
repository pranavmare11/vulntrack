from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_str
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Profile
from django.http import HttpResponse
from .models import Post, Reaction
from .forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404



# Create your views here.
def home(request):
    return render(request, 'vulnerabilities/home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Make sure the user has a Profile
            Profile.objects.get_or_create(user=user)

            auth_login(request, user)
            return redirect('profile')

        else:
            return render(request, 'vulnerabilities/login.html', {
                'error': 'Invalid username or password.'
            })

    else:
        return render(request, 'vulnerabilities/login.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password') or ''
        confirm_password = request.POST.get('confirm_password') or ''

        if not username or not email or not password:
            return render(request, 'vulnerabilities/register.html', {
                'error': 'All fields are required.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'vulnerabilities/register.html', {
                'error': 'Username already exists.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'vulnerabilities/register.html', {
                'error': 'An account with this email already exists.'
            })

        if password != confirm_password:
            return render(request, 'vulnerabilities/register.html', {
                'error': 'Passwords do not match.'
            })

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'vulnerabilities/register.html', {
                'error': ' '.join(e.messages)
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return render(request, 'vulnerabilities/register.html', {
                'error': 'Username already exists.'
            })

        auth_login(request, user)
        return redirect('profile')

    return render(request, 'vulnerabilities/register.html')     

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                reverse('reset-password', kwargs={'uidb64': uid, 'token': token})
            )

            send_mail(
                subject='Password Reset Requested',
                message=f'Click the link to reset your password: {reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

        # Always show the same message (avoids leaking which emails exist)
        return render(request, 'vulnerabilities/forgot-password.html', {
            'message': 'If an account with that email exists, a reset link has been sent.'
        })

    return render(request, 'vulnerabilities/forgot-password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not new_password or not confirm_password:
                return render(request, 'vulnerabilities/reset-password.html', {
                    'error': 'Both password fields are required.'
                })
            if new_password != confirm_password:
                return render(request, 'vulnerabilities/reset-password.html', {
                    'error': 'Passwords do not match.'
                })
            try:
                validate_password(new_password, user=user)
            except ValidationError as e:
                return render(request, 'vulnerabilities/reset-password.html', {'error': ' '.join(e.messages)})

            user.set_password(new_password)
            user.save()
            return render(request, 'vulnerabilities/reset_done.html')
        return render(request, 'vulnerabilities/reset-password.html')
    else:
        return render(request, 'vulnerabilities/reset_invalid.html')

@login_required
def profile(request):

    if not request.user.is_authenticated:
        return HttpResponse("Login required", status=401)
    profile = request.user.profile

    if request.method == "POST":

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]
            profile.save()

        return redirect("profile")

    return render(request, "vulnerabilities/profile.html")

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("explore")
    else:
        form = PostForm()
    return render(request, "vulnerabilities/create_post.html", {"form": form})

@login_required
def explore(request):
    post = Post.objects.select_related('author').all().order_by('-created_at')
    return render(request, "vulnerabilities/explore.html", {"posts": post})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    user_reaction = None
    if request.user.is_authenticated:
        r = Reaction.objects.filter(post=post, user=request.user).first()
        user_reaction = r.value if r else None

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/accounts/login/?next={request.path}")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=post.pk)

    return render(request, "vulnerabilities/post_detail.html", {
        "post": post,
        "comments": post.comments.select_related("author"),
        "form": form,
        "user_reaction": user_reaction,
    })


@login_required
@require_POST
def react(request, pk, action):
    post = get_object_or_404(Post, pk=pk)
    value = Reaction.LIKE if action == "like" else Reaction.DISLIKE
    reaction, created = Reaction.objects.get_or_create(
        post=post, user=request.user, defaults={"value": value}
    )
    if not created:
        if reaction.value == value:
            reaction.delete()          # clicking again removes your reaction
        else:
            reaction.value = value     # switch like <-> dislike
            reaction.save()
    return redirect(request.META.get("HTTP_REFERER") or post.get_absolute_url())

def regisert_user(request):
    return render(request, 'vulnerabilities/regisert_user.html')

@login_required
def my_finding(request):
    posts = list(
        Post.objects.filter(author=request.user)
        .prefetch_related("reactions")
    )

    total_posts = len(posts)

    total_likes = sum(
        post.likes_count for post in posts
    )

    total_dislikes = sum(
        post.dislikes_count for post in posts
    )

    return render(
        request,
        "vulnerabilities/my_finding.html",
        {
            "posts": posts,
            "total_posts": total_posts,
            "total_likes": total_likes,
            "total_dislikes": total_dislikes,
        },
    )