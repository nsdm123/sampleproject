from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=200)
    book_content = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.book_name} by {self.author}"
