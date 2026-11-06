from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta


from .models import User, Rank, Habit, DailyLog, Comment
from .forms import HabitForm

import json

# Create your views here.



def index(request):
    leaderboard = User.objects.order_by('-total_xp')[:10]
    return render(request, 'habit/index.html', {"leaderboard": leaderboard})


def top_habit(request):
    leaderboard = Habit.objects.order_by('-longest_streak')[:10]
    return render(request, 'habit/tophabits.html', {"leaderboard": leaderboard})



@login_required
def add_comment(request, profile_id):
    if request.method == "POST":
        # 1. Parse the JSON data sent by the Fetch API
        data = json.loads(request.body)
        
        # 2. Grab the exact user instance, not a list
        receiver = get_object_or_404(User, pk=profile_id)
        
        # 3. Create the comment using your exact model field names
        new_comment = Comment.objects.create(
            poster=request.user,
            receiver=receiver,
            comment=data.get('comment', '')
        )
        
        # 4. Return the exact JSON dictionary your JavaScript expects
        return JsonResponse({
            "status": "success", 
            "username": new_comment.poster.username,
            "comment": new_comment.comment,
            "formatted_time": new_comment.formatted_time
        })



@login_required
def add_habit(request):
    user = request.user

    if request.method == "POST":
        form = HabitForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            try:
                Habit.objects.create(user=request.user,
                                    name=name, 
                                    description=description,
                                    current_streak=0,
                                    longest_streak=0)
                return HttpResponseRedirect(reverse('dashboard', kwargs={"id":request.user.id}))
            except IntegrityError:
                return render(request, "habit/error.html", {"message": "Habit with same name exits"})
        else:
            message = "Error submiting the form.Try Again!!"
            return render(request,"habit/error.html", {"message": message})

    else:
        form = HabitForm()
        return render(request, "habit/add_habit.html", {"form":form})



@login_required
def delete_habit(request):

    if request.method == "POST":
        data = json.loads(request.body) #unpacking the json sent by dashboard.js

        habit_id = data.get('habit_id')
        if not habit_id:
            return JsonResponse({"error": "No habit_id found"}, status=400)

        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        habit.delete()
        
        return JsonResponse({"status": "success"})       


@login_required
def update_log(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        habit_id = data.get('habit_id')
        if not habit_id:
            return JsonResponse({"error": "No habit_id found"}, status=400)
            
        habit = Habit.objects.get(id=habit_id, user=request.user)
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # Fetch or create the log, but do not rely on the 'created' boolean
        log, created = DailyLog.objects.get_or_create(habit=habit, date_logged=today)
        leveled_up = False
        
        # FIX 1: Lock out duplicate clicks by checking the completion status
        if not log.is_completed:    
            log.is_completed = True
            log.save()

            # Calculating streak
            last_log = DailyLog.objects.filter(
                habit=habit,
                is_completed=True,
                date_logged__lt=today
            ).order_by('-date_logged').first()

            # FIX 2: Execute the math directly without a contradictory boolean check
            if last_log and last_log.date_logged == yesterday:
                habit.current_streak += 1
            else:
                habit.current_streak = 1

            if habit.current_streak > habit.longest_streak:
                habit.longest_streak = habit.current_streak
            
            habit.save()

            # Updating xp given
            request.user.total_xp += 500
            request.user.save()
            leveled_up = request.user.check_and_update_rank()
            
            formatted_date = today.strftime("%b %d, %Y")

            badge_url = None
            rank = None
            if request.user.current_rank and request.user.current_rank.rank_badge and leveled_up:
                badge_url = request.user.current_rank.rank_badge.url
                rank = request.user.current_rank.rank_title
            
            return JsonResponse({
                "status": "success",
                "is_completed": log.is_completed,
                "current_streak": habit.current_streak,
                "total_xp": request.user.total_xp,
                "new_rank_title": rank,
                "new_rank_badge": badge_url,
                "last_logged_date": formatted_date,
                "total_xp": request.user.total_xp,
            })
            
        else:
            # If the log is already marked True, ignore the click to stop XP farming
            return JsonResponse({
                "status": "ignored", 
                "message": "Already completed today"
            })


@login_required
def dashboard(request, id):
    profile_user = get_object_or_404(User, pk=id)

    habits = Habit.objects.filter(user=profile_user)

    comments = Comment.objects.filter(receiver=profile_user).order_by('-timestamp')

    return render(request, "habit/dashboard.html", {
        "profile_user":profile_user,
        "habits":habits,
        "comments":comments
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "habit/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "habit/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "habit/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "habit/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "habit/register.html")