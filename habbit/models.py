from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

# Create your models here.


# Store all ranks in one model and let User point to it
class Rank(models.Model):

    rank_title = models.CharField("Rank", default="Recruit", max_length=30)
    rank_badge = models.ImageField("Badge Image", 
    upload_to="ranks/",
    default="ranks/default.png"
    )
    xp_needed = models.IntegerField(default=1000)
    celebratory_message = models.CharField(null=True, max_length=250, blank=True) 

    class Meta:
        ordering = ["-xp_needed"]

    def __str__(self):
        return f"{self.rank_title} requires {self.xp_needed}XP with celebratory message: {self.celebratory_message}"
    


class User(AbstractUser):
    
    email = models.EmailField(unique=True, null=False, blank=False)
    total_xp = models.IntegerField(default=0)
    current_rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True,related_name="user")


    def __str__(self):
        return f"{self.username} {self.last_name} with emailId: {self.email}, TotalXP: {self.total_xp} holds {self.current_rank} Rank"
    
    def check_and_update_rank(self):

        from .models import Rank

        eligible_rank = Rank.objects.filter(xp_needed__lte=self.total_xp).order_by("-xp_needed").first()
        if eligible_rank and eligible_rank != self.current_rank:
            self.current_rank = eligible_rank
            self.save()
        return self.current_rank

    def save(self, *args, **kwargs):
        # Automatically re-calculate rank whenever the profile is saved
        self.check_and_update_rank()
        super().save(*args, **kwargs)


class Habit(models.Model):
    
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,related_name="Habits", on_delete=models.CASCADE)
    name = models.CharField(_("Habit Name"), max_length=50)
    description =  models.TextField(max_length=100, null=True, blank=True)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'name')

    @property
    def completed_today(self):
        today = timezone.now().date()
        return self.daily_logs.filter(date_logged=today, is_completed=True).exists()


    @property
    def last_logged_date(self):
        """Returns the date of the most recent completed log."""
        last_log = self.daily_logs.filter(is_completed=True).order_by('-date_logged').first()
        if last_log:
            return last_log.date_logged.strftime("%b %d, %Y")
        return None

    def __str__(self):
        return f"{self.name} Habit created by {self.user}"
    


class DailyLog(models.Model):

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="daily_logs")
    date_logged = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date_logged')

    @property
    def msg(self):
        if self.is_completed:
            return f"Completed Task at {self.date_logged}"
        return f"Task not completed"

    def __str__(self):
        return f"{self.habit}: {self.msg}"
    

class Comment(models.Model):

    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="comment_posted"
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        blank = True,
        null=True,
        related_name= "comment_received"
    ) 
    comment = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def formatted_time(self):
        if self.timestamp:
            return self.timestamp.strftime("%d %B at %I%p").lower()
        return "unknown time"

    def __str__(self):
        return f'''
                {self.poster}: 
                    {self.comment} {self.formatted_time}'''

@receiver(post_save, sender=User)
def assign_default_rank(sender, instance, created, **kwargs):
    """Automatically assigns the lowest tier Rank to freshly registered users."""
    if created:
        # Dynamically grabs the Rank model using exact string references[cite: 1]
        Rank = apps.get_model('habbit', 'Rank')
        
        # Order by xp_needed ascending and grab the very first one (lowest XP)
        starter_rank = Rank.objects.order_by('xp_needed').first()
        
        if starter_rank:
            instance.current_rank = starter_rank
            instance.save()