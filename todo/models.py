from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    like_count = models.IntegerField(default=0)
    love_count = models.IntegerField(default=0)
    wow_count = models.IntegerField(default=0)

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
