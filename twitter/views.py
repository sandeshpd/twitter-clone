from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet, Comment
from .forms import TweetForm, SignUpForm, UpdateUserForm, ProfilePicForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 

# Create your views here.

# Homepage
def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ('Your tweet has been posted!'))
                return redirect('home')

        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'tweets':tweets, 'form':form})
    else:
        messages.success(request, ('You must log in to proceed.'))
        return redirect('login')
        # tweets = Tweet.objects.all().order_by('-created_at')
        # return render(request, 'home.html', {'tweets':tweets})


# List of profiles
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profile_list.html', {'profiles':profiles})
    else:
        messages.success(request, ('You must log in to proceed.'))
        return redirect('home')

# Unfollow User
def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id = pk)
        # Unfollow profile you got
        request.user.profile.follows.remove(profile)
        # Save profile
        request.user.profile.save()

        messages.success(request, (f'You unfollowed @{ profile.user.username }.'))
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, ('You must login to proceed.'))
        return redirect('home')

# Follow User
def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id = pk)
        # Unfollow profile you got
        request.user.profile.follows.add(profile)
        # Save profile
        request.user.profile.save()

        messages.success(request, (f'You followed @{ profile.user.username }.'))
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, ('You must login to proceed.'))
        return redirect('home')



# User profile  
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        tweets = Tweet.objects.filter(user_id = pk).order_by('-created_at')

        # POST form logic
        if request.method =='POST':
            # Get current user
            current_user = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Determine to follow or unfollow
            if action == 'unfollow':
                current_user.follows.remove(profile)
            elif action == 'follow':
                current_user.follows.add(profile)
            # Save the current profile
            current_user.save()

        return render(request, 'profile.html', {'profile':profile, 'tweets':tweets})
    else:
        messages.success(request, ('You must log in first to view this profile.'))
        return redirect('home')
    
# Searching users
def search_user(request):
    if request.method == 'POST':
        search = request.POST['search']
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_user.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search_user.html', {})


# Followers Page
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'followers.html', {'profiles':profiles})
        else:
            messages.success(request, ("You don't have permission to view other people's followers."))
            return redirect('home')
    else:
        messages.success(request, ('You must log in to proceed.'))
        return redirect('home')
    
# People that User Follows
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'follows.html', {'profiles':profiles})
        else:
            messages.success(request, ("You don't have permission to view other people's followers."))
            return redirect('home')
    else:
        messages.success(request, ('You must log in to proceed.'))
        return redirect('home')

# User Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You Have Been Successfully Logged In. Enjoy Tweeting!'))
            return redirect('home')
        else:
            messages.success(request, ('Something is Wrong. Please Try Again!'))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

# User Logout
def logout_user(request):
    logout(request)
    messages.success(request, ('You Have Been Logged Out.'))
    return redirect('login')

# Signing Up User
def signup_user(request):
        form = SignUpForm()
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']

                # Log In user
                user = authenticate(username = username, password = password)
                login(request, user)
                messages.success(request, ('You\'ve been registered Successfully. Welcome to Twitter!'))
                return redirect('home')

        return render(request, 'signup.html', {'form':form})

# Updating User Info
def update_user(request):
        if request.user.is_authenticated:
            current_user = User.objects.get(id = request.user.id)
            profile_user = Profile.objects.get(user__id = request.user.id)
            user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance = current_user)
            profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance = profile_user)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                # login(request, current_user)
                messages.success(request, ('Your Profile Is Updated.'))
                return redirect('home')
            
            return render(request, 'update_user.html', {'user_form':user_form, 'profile_form':profile_form})
        else:
            messages.success(request, ('You must login to proceed.'))
            return redirect('home')

# Change the Password        
def change_password(request):
    return render(request, 'change_password.html', {})
        
# Like or Unlike tweet
def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id = pk)
        if tweet.likes.filter(id = request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        # print(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ('You must login to perform this action'))
        return redirect('home')
    
# Comment under tweet
def tweet_comment(request, pk):
    if request.user.is_authenticated:
        tweet = Tweet.objects.get(id = pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit = False)
                comment.user = request.user
                comment.tweet = tweet
                comment.save()
                form = CommentForm()
        
                tweet.save()
                return redirect('tweet_comment', pk = pk)
        else:
            form = CommentForm()

        comments = tweet.comments.all().order_by('-created_at')
        return render(request, 'tweet_comment.html', {'tweet': tweet, 'form':form, 'comments':comments})
    else:
        messages.success(request, ('You must login to proceed.'))
        return redirect('home')


# Share the tweet
def tweet_share(request, pk):
    tweet = get_object_or_404(Tweet, id = pk)
    if tweet:
        return render(request, 'tweet_share.html', {'tweet':tweet})
    else:
        messages.success(request, ('This tweet does not exist.'))
        return redirect('home')
    
# Deleting Tweet
def tweet_delete(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id = pk)
        # Check if intended tweet really belong to the true user
        if request.user.username == tweet.user.username:
            tweet.delete()
            messages.success(request, ('The tweet is deleted.'))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, ('You don\'t have permission to delete this tweet.'))
            return redirect('home')
    else:
        messages.success(request, ('You must login first to proceed.'))
        return redirect(request.META.get('HTTP_REFERER'))

# Bookmarking Tweet
def save_bookmark_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id = pk)
        if tweet.bookmarks.filter(id = request.user.id):
            tweet.bookmarks.remove(request.user)
            messages.success(request, ('The post has been removed from bookmarks.'))
        else:
            tweet.bookmarks.add(request.user)
            messages.success(request, 'The post has been saved in bookmarks.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ('You must login to proceed.'))
        return redirect('home')

# Showing Bookmarks page    
def show_bookmark_tweet(request):
    bookmarked_tweets = request.user.tweet_bookmark.all()
    return render(request, ('tweet_bookmark.html'), {'bookmarked_tweets':bookmarked_tweets})
