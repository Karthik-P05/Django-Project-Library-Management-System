from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime,timedelta

class User(AbstractUser):
    usertype = models.CharField(max_length=100)
    
class Member(models.Model):
    member_id = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=150)
    department = models.CharField(max_length=255)
    year_of_study = models.IntegerField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='images/', default='images/default_profile.jpg')
    status = models.BooleanField(default=False)
    
class Librarian(models.Model):
    librarian_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='images/')
    

# class Author(models.Model):
#     name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.name
    
# class Genre(models.Model):
#     name = models.CharField(max_length=100, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=255)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    # genres = models.ForeignKey(Genre, on_delete=models.CASCADE)
    genres = models.CharField(max_length=150)
    copies_available = models.PositiveBigIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    book_cover = models.ImageField(upload_to="book_cover/", default='book_cover/default_cover.jpg')
    book_upload = models.FileField(upload_to="e-book/", default='e-book/default_book.jpg')
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
def expiry():
    return datetime.today() + timedelta(days=14)
class Borrowing(models.Model):
    # borrow_id = models.
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    # due_date = models.DateField()
    due_date = models.DateField(default=expiry)
    returned_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.username}"



class Reservation(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    reservation_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('Reserved', 'Reserved'), ('Available', 'Available')])

    def __str__(self):
        return f"{self.book.title} reserved by {self.member.username}"

class Review(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Review of {self.book.title} by {self.member.username}"
    