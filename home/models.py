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
    status = models.BooleanField(default=True)
    
    

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


    
    # def calculate_fine(self):
    #     if self.returned and self.return_date and self.due_date:
    #         if self.return_date > self.due_date:
    #             days_late = (self.return_date - self.due_date).days
    #             self.fine_amount = days_late * 10  # Assuming fine is 10 per day
    #             self.save()
    #     return self.fine_amount
    




class Reservation(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ), default='pending')

    class Meta:
        ordering = ['reservation_date']
    

class Review(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    review_text = models.TextField(max_length=1000)
    review_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Review of {self.book.title} by {self.member.username}"
    
    
class Payment(models.Model):
    name = models.CharField(max_length=100)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=100, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    purchased_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)    
    
    
    
class Borrowing_details(models.Model):
    # borrow_id = models.
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Returned', 'Returned'),
    ]

    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_request')
    approved_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    returned_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    days_overdue = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    fine_paid = models.BooleanField(default=False) 


    def calculate_fine(self):
        if self.fine_paid or self.returned:
            return
        today = timezone.now().date()
        if self.due_date and today > self.due_date:
            days_late = (today - self.due_date).days
            self.fine_amount = days_late * 5  # ₹5 per day late
            self.save()
            
class Fine_Payment(models.Model):
    name = models.CharField(max_length=200)  # Name of the book or payment description
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # Member making the payment
    borrow_id = models.ForeignKey(Borrowing_details, on_delete=models.CASCADE, null=True, blank=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Book associated with the payment
    book_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Fine amount
    razorpay_order_id = models.CharField(max_length=100)  # Razorpay order ID
    razorpay_payment_id = models.CharField(max_length=100)  # Razorpay payment ID
    razorpay_payment_status = models.CharField(max_length=50)  # Payment status (e.g., success, failed)
    paid = models.BooleanField(default=False)  # Payment status (paid or not)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of payment creation

    def __str__(self):
        return f"Payment #{self.id} - {self.member.name}"
    
    
class Wishlist(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    saved_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.book.title} saved by {self.member.username}"