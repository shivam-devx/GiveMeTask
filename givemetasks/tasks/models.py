from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    priority = models.CharField(max_length=10,choices=[
        ('High','High'),
        ('Medium','Medium'),
        ('Low','Low')
    ])

    completed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    due_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.title