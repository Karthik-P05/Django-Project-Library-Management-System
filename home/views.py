from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Member, Book, Librarian, Payment, Review, Borrowing_details, Fine_Payment, Wishlist, Reservation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from django.utils.timezone import now
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, When, Value, IntegerField
import json
import razorpay


# Create your views here.



User = get_user_model()


def member_reg(request):
    if request.method == "POST":
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']  
            username = request.POST['username']  
            password  = request.POST['password']
            confirm_password  = request.POST['confirm_password']   
            email  = request.POST['email']   
            phone = request.POST['phone']  
            student_id  = request.POST['student_id']  
            department  = request.POST['department']  
            year  = request.POST['year']
            image = request.FILES.get('profile_picture')
            address = request.POST['address']    
        
            if User.objects.filter(username=username).exists():
                # messages.error(request, "Username is already taken.")
            #     # return redirect('index_of_home')
                # return HttpResponse("<script>alert('Username is already taken');window.location.href='http://127.0.0.1:8000/';</script>")
                return JsonResponse({
                        'status': 'error',
                        'message': 'Username is already taken.'
                    }, status=400)
                
            if password != confirm_password:
                # messages.error(request, "Passwords do not match.")
                # return redirect('index_of_home')
                # return HttpResponse("<script>alert('Password do not match');window.location.href='http://127.0.0.1:8000/#register';</script>")
                return JsonResponse({
                        'status': 'error',
                        'message': 'Passwords do not match.'
                    }, status=400)
                               

            if User.objects.filter(email=email).exists():
                # messages.error(request, "Email is already registered.")
            #     # return redirect('index_of_home')
                # return HttpResponse("<script>alert('Email is already taken');window.location.href='http://127.0.0.1:8000/';</script>")
                return JsonResponse({
                        'status': 'error',
                        'message': 'Email is already registered.'
                    }, status=400)
                
            if Member.objects.filter(student_id=student_id).exists():
                return JsonResponse({
                        'status': 'error',
                        'message': 'Student ID already exists.'
                    }, status=400)
                
                
            user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email, usertype='Student',is_active=False,is_staff=False)
            user.save()
            
            member=Member.objects.create(member_id=user, student_id = student_id, year_of_study = year, department = department, phone_number=phone,address=address, status=True, profile_picture = image)
            member.save()
        
        # return HttpResponse("<script>alert('Request for Registration Completed');window.location.href='http://127.0.0.1:8000/';</script>")
            return JsonResponse({
                'status': 'success',
                'message': 'Registration request submitted successfully! Your account will be activated after approval.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=500)
                
    else:
        return render(request,'home-front-page.html')
        
        
        
def logins(request):
    if request.method=='POST':
        USERNAME=request.POST['username']
        PASSWORD=request.POST['password']
        print(USERNAME)
        print(PASSWORD)
        
        try:
            user = User.objects.get(username=USERNAME)
            
            # Check if the user is inactive
            if not user.is_active:
                messages.error(request, 'Your account is pending for approval. Cannot login.')
                return render(request, 'home-page-login-base.html')
        
            userpass = authenticate(request, username=USERNAME, password=PASSWORD)
            if userpass is not None:
                print("1",userpass)
            
                if userpass.is_superuser==1:
                    print('admin')
                    login(request, userpass)
                    request.session['addmin_id']=userpass.id
                    return redirect('admin_homepage')
                    # return HttpResponse("<script>window.location.href='http://127.0.0.1:8000/home/homepage/';</script>")
            
        
                elif userpass.is_staff==1:
                    print('librarian')
                    login(request, userpass)
                    request.session['lib_id']=userpass.id
                    return redirect('librarian_homepage')
            
                 
                elif userpass.is_active==1:
                    # Check if the user is a member and their status is True
                    try:
                        member = Member.objects.get(member_id=userpass)
                    
                        if member.status == True:  # Check if member.status is True
                            print('member')
                            login(request, userpass)
                            request.session['stud_id']=userpass.id
                            return redirect('member_homepage')
                        else:
                            # Member status is False (blocked)
                            messages.error(request, 'Your account is now being blocked. Contact the admin.')
                            return render(request, 'home-page-login-base.html')
            
                    except Member.DoesNotExist:
                        # User is not a member
                        messages.error(request, 'Invalid member account.')
                        return render(request, 'home-page-login-base.html')
                
            # elif userpass.is_active==False:
            #     messages.error(request, 'Your account is pending for approval. Cannot login.')
            #     return render(request, 'login.html')
                
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'home-page-login-base.html')
            
        except User.DoesNotExist:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')
            return render(request, 'home-page-login-base.html')
        
        # elif userpass is not None and not userpass.is_active:
        #     print('pending request')
        #     # login(request, userpass)
        #     return HttpResponse("<script>alert('Your account is pending approval.');window.location.href='http://127.0.0.1:8000/login';</script>")
            
        #     return render(request, 'login.html', {'error': 'Your account is pending approval.'})
        
        # else:
        #     # return HttpResponse('Invalid Login')
        #     return HttpResponse("<script>alert('Username or Password doesnot exist!');window.location.href='http://127.0.0.1:8000/login';</script>")
            
        
    else:
        return render(request, 'home-page-login-base.html')
 

def logouts(request):
    logout(request)
    return redirect(logins)        

def admin_home(request):
    # return HttpResponse("Welcome")
    # return render(request, 'admin-starter-page.html')
    # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    new_requests_count = User.objects.filter(is_active=0).count()
    issue_count = Borrowing_details.objects.filter(status = "Pending").count()
    context = {
        'new_requests_count': new_requests_count,
        'new_issue' : issue_count,
    }
    return render(request, 'admin-home-main.html', context)
    # return render(request, 'admin-index_of_admin.html')
    
def view_studentlist(request):
    students = Member.objects.select_related('member_id').filter(member_id__is_active=True)
    return render(request,'admin-studentlist.html',{'student_list':students})


def edit_student(request, member_id):
    try:
        # member = Member.objects.get(id=member_id)
        member = Member.objects.select_related('member_id').get(id=member_id)
        # user = User.objects.get(id=member_id)
        data = {
            'id': member.id,
            'student_id': member.student_id,
            'department': member.department,
            'year_of_study': member.year_of_study,
            'phone': member.phone_number,
            'address': member.address,
            'email': member.member_id.email,
            
        }
        return JsonResponse(data)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

@csrf_exempt
def update_member(request, member_id):
    if request.method == 'POST':
        
        member = Member.objects.get(id=member_id)
        user = member.member_id
            
            # Update User (email)
        user.email = request.POST.get('email')
        user.save()
            
            # Update Member
        member.student_id = request.POST.get('student_id')
        member.department = request.POST.get('department')
        member.year_of_study = request.POST.get('year_of_study')
        member.phone_number = request.POST.get('phone')
        member.address = request.POST.get('address')
        member.save()
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def admin_delete_member(request,id):
    stud = Member.objects.get(id=id)
    user_id = stud.member_id.id
    stud.delete()
    User.objects.filter(id=user_id).delete()
    return redirect('view_studentlist')



def student_request(request):
    # x=Member.objects.select_related('member_id').filter(member_id__is_active=False)
    # mem=Member.objects.select_related('member_id').all()
    # mem = Member.objects.all().order_by('-id')
    mem = Member.objects.order_by('member_id__is_active', '-id')

    return render(request,'admin-student-request.html',{'student_req':mem})


def admin_approve_student(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    
    stud.member_id.is_active = True
    stud.member_id.save()
    return redirect('student_request')


def admin_delete_student(request,id):
    stud = Member.objects.get(id=id)
    user_id = stud.member_id.id
    stud.delete()
    User.objects.filter(id=user_id).delete()
    return redirect('student_request')




# def admin_view_member(request, id):
#     print(id)
#     # stud = Member.objects.get(id=id)
#     stud = Member.objects.select_related(d).all()
#     # user_id = stud.member_id.id
#     # user = User.objects.get(id=user_id)
#     # print(user)
#     # stud = get_object_or_404(Member, id)
#     # stud = Member.objects.all()
#     return render(request,'studentlist.html',{'view':stud})
    # return render(request,'view_student.html')


def admin_add_members(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']  
        username = request.POST['username']  
        password  = request.POST['password']
        confirm_password  = request.POST['confirm_password']   
        email  = request.POST['email']   
        phone = request.POST['phone']  
        student_id  = request.POST['student_id']  
        department  = request.POST['department']  
        year  = request.POST['year']
        image = request.FILES.get('profile_picture')
        address = request.POST['address']    
        
        
        if password != confirm_password:
            # messages.error(request, "Passwords do not match.")
            # return redirect('index_of_home')
            messages.error(request, "Passwords do not match!")
            return redirect('add_member')
            # return HttpResponse("<script>alert('Password do not match');window.location.href='http://127.0.0.1:8000/adminaddmembers/';</script>")
            

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another!")
            return redirect('add_member')
        #     # messages.error(request, "Username is already taken.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Username is already taken');window.location.href='http://127.0.0.1:8000/adminaddmembers/script>")
            

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use another email!")
            return redirect('add_member')
        #    return HttpResponse("<script>alert('Email is already taken');window.location.href='http://127.0.0.1:8000/adminaddmembers/';</script>")
            
        try:    
            user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email, usertype='Student',is_active=True,is_staff=False)
            user.save()
            
            member=Member.objects.create(member_id=user, student_id = student_id, year_of_study = year, department = department, phone_number=phone,address=address, status=True, profile_picture = image)
            member.save()
            messages.success(request, "Student added successfully!")
            return redirect('add_member')
        
        except Exception as e:
            # Return error response
            messages.error(request, f"Error: {str(e)}")
            return redirect('add_member')
        
        # return HttpResponse("<script>alert('Request for Registration Completed');window.location.href='http://127.0.0.1:8000/studentlist/';</script>")
                
    else:    
    
        return render(request, 'admin-add-student.html')



def admin_activate_member(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    stud.status = True
    stud.save()
    return redirect('view_studentlist')

def admin_deactivate_member(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    stud.status = False
    stud.save()
    return redirect('view_studentlist')


def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        publish = request.POST['publication_date']
        b_cover = request.FILES.get('cover')
        book = request.FILES.get('book')
        genre = request.POST['genre']
        copies = request.POST['copies']
        about = request.POST['description']
        price = request.POST['price']
        
        
        if Book.objects.filter(title=title).exists():
            messages.error(request, "Book already exists!")
            return redirect('add_book')
        
        try:
            # Create and save the book
            book = Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                publication_date=publish,
                book_cover=b_cover,
                book_upload=book,
                genres=genre,
                copies_available=copies,
                description=about,
                rate=price
            )
            book.save()
            
            # Return success response
            # return HttpResponse('success:Book added successfully!')
            messages.success(request, "Book added successfully!")
            return redirect('add_book')
        except Exception as e:
            # Return error response
            messages.error(request, f"Error: {str(e)}")
            return redirect('add_book')
            # return redirect('add_book_page')
            # return HttpResponse(f'error:Failed to add book: {str(e)}')
    else:
        return render(request, 'admin-add-book.html')
        
    #     book = Book.objects.create(title = title, author = author, isbn = isbn, publication_date = publish, book_cover = b_cover, book_upload = book, genres = genre, copies_available = copies, description = about, rate = price )
    #     book.save()
        
    #     return HttpResponse("<script>alert('Book Addeed Successfully');window.location.href='http://127.0.0.1:8000/homepage/';</script>")
        
    # else:
    #     return render(request, 'admin-addbook.html')
    # # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    # return render(request, 'admin-index_of_admin.html')
    
def admin_add_librarian(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']  
        username = request.POST['username']  
        password  = request.POST['password']
        confirm_password  = request.POST['confirm_password']   
        email  = request.POST['email']   
        phone = request.POST['phone']  
        image = request.FILES.get('profile_picture')
        address = request.POST['address']    
        
        
        if password != confirm_password:
            # messages.error(request, "Passwords do not match.")
            # return redirect('index_of_home')
            # return HttpResponse("<script>alert('Password do not match');window.location.href='http://127.0.0.1:8000/adminaddlibrarian/';</script>")
            messages.error(request, "Passwords do not match!")
            return redirect('add_librarian')
            
            

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already exists!")
            return redirect('add_librarian')
        #     # messages.error(request, "Username is already taken.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Username is already taken');window.location.href='http://127.0.0.1:8000/adminaddlibrarian/script>")
            

        if User.objects.filter(email=email).exists():
            messages.error(request, "Your Email is already registered!")
            return redirect('add_librarian')
        #     # messages.error(request, "Email is already registered.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Email is already taken');window.location.href='http://127.0.0.1:8000/adminaddlibrarian/';</script>")
            
        try:    
            user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email, usertype='Librarian',is_active=True,is_staff=True)
            user.save()
        
            lib=Librarian.objects.create(librarian_id=user, phone_number=phone,address=address, profile_picture = image)
            lib.save()
        
            # return HttpResponse("<script>alert('Librarian Added');window.location.href='http://127.0.0.1:8000/homepage/';</script>")
            messages.success(request, "Librarian added successfully!")
            return redirect('add_librarian')
        
        except Exception as e:
            # Return error response
            messages.error(request, f"Error: {str(e)}")
            return redirect('add_librarian')
                
    else:    
    
        return render(request, "admin-add-librarian.html")
    
    
def member_homepage(request):
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    user = User.objects.get(id=memb)
    return render(request, 'member-home-page.html',{'view':member,'data':user})
    # return render(request, 'index.html')
    # return render(request, 'starter-page.html')
    
    # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    # return render(request, 'admin-index_of_admin.html')


    
    
def search_book(request):
    if request.method == "POST":
        search = request.POST['search']
        request.session['search_query'] = search
        print(search)
        
        if search:
            book = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search) | Book.objects.filter(isbn__icontains=search)
        else:
            book = Book.objects.none()
                    
        return render(request, 'member-search-result.html', {'results': book, 'search':search})
    else:
        # return render(request, 'member-home_page.html')
        search = request.session.get('search_query', '')
        if search:
            book = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search) | Book.objects.filter(isbn__icontains=search)
        else:
            book = Book.objects.none()
        
        return render(request, 'member-search-result.html', {'results': book, 'search': search})
    
    
def view_book(request,id):
    # print(id)
    
    book = Book.objects.get(id=id)
    
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    
    reviews = Review.objects.filter(book_id_id = book)
    
    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / len(reviews) if reviews else 0
    
    submitted = Review.objects.filter(book_id_id = book, member_id_id = member)
    
    related_books = Book.objects.filter(genres = book.genres).exclude(id=book.id)[:4]
        
    # book_payment = Payment.objects.get(member_id_id=member, book_id_id=book.id)
    try:
        book_payment = Payment.objects.get(member_id_id=member, book_id_id=book)
    except Payment.DoesNotExist:
        # Handle case where payment does not exist
        book_payment = None
       
        
    # borrow = Borrowing_details.objects.get(member_id_id=member, book_id_id=book)
    try:
        # borrow = Borrowing_details.objects.get(member_id=member, book_id=book)
        borrow = Borrowing_details.objects.filter(member_id=member, book_id=book).order_by('-id').first()
    except Borrowing_details.DoesNotExist:
        borrow = None  # No borrow record found
    # print(borrow.status)
    
    wishlist_books = Wishlist.objects.filter(member_id_id=member, book_id_id=book)

    

        
    return render(request,"member-book-view.html", {
        'book' : book, 
        'review_submitted' : submitted.exists(),
        'related_books' : related_books,
        'payment':book_payment,
        'reviews':reviews,
        'average_rating': round(average_rating, 1),
        'borrow_request' : borrow,
        'wishlist_books' : wishlist_books
        
        } )

def checkout_ebook(request, id):
    
    book = Book.objects.get(id=id)
    request.session['book_id'] = book.id
    
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    user = User.objects.get(id=memb)

    return render(request, 'e-book-django.html',{'view':member,'data':user, 'book':book})



# rzp_test_bgOiUnm7YgSzuu,BKg6Lpv9pn5sMEwwP1Wecd0I

RAZORPAY_API_KEY = 'rzp_test_bgOiUnm7YgSzuu'
RAZORPAY_API_SECRET = 'BKg6Lpv9pn5sMEwwP1Wecd0I'



import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

@csrf_exempt
def create_razorpay_order(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount')) 
        currency = 'INR'
        receipt = 'order_rcptid_11'

        try:
            order = client.order.create({
                'amount': amount,
                'currency': currency,
                'receipt': receipt,
                'payment_capture': 1  # Auto-capture payment
            })
            return JsonResponse({'order_id': order['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            # Payment is successful and verified
            
            # Fetch the member and book details from the session or request
            member_id = request.session.get('stud_id')  # Assuming member ID is stored in session
            book_id = request.session.get('book_id')  # Retrieve book_id from session
            book_rate = request.POST.get('book_rate')  # Pass book_rate from the frontend
            book_name = request.POST.get('book_name')  # Pass book_name from the frontend
        
            member = get_object_or_404(Member, member_id_id=member_id)
            book = get_object_or_404(Book, id=book_id)
            # member = Member.objects.get(member_id_id=member_id)
            # book = Book.objects.get(id=book_id)
            
            
            print("****")
            # Save payment details to the database
            payment = Payment(
                    name=book_name,  
                    member_id=member,
                    book_id=book,
                    book_rate=book_rate,
                    razorpay_order_id=razorpay_order_id,
                    razorpay_payment_status='success',
                    razorpay_payment_id=razorpay_payment_id,
                    paid=True
                )
            payment.save()
        
            if 'book_id' in request.session:
                del request.session['book_id']
            
            return JsonResponse({'status': 'success'})
        except razorpay.errors.SignatureVerificationError:
            # Payment verification failed
            return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)
        except Exception as e:
            # Handle other exceptions
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def view_pdf(request, id):
    book = get_object_or_404(Book, id=id)
    # book = Book.objects.get(id=id)
    file_path = book.book_upload.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def review_and_rating(request):
    if request.method == "POST":
        book_id = request.POST.get('bookid')
        book = get_object_or_404(Book, id=book_id)
        
        member_id = request.session.get('stud_id')
        member = get_object_or_404(Member, member_id_id=member_id)
        
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        # print("qqqqq")
        reviewed = Review(
                    member_id = member,
                    book_id = book,
                    rating = rating,
                    review_text = review
                )
        reviewed.save()
        
        return redirect(view_book, id = book_id)
        
def borrow_request(request, id):

    book = Book.objects.get(id=id)
    
    member_id = request.session.get('stud_id')
    member = get_object_or_404(Member, member_id_id=member_id)
    
    
    if book.copies_available > 0:
        Borrowing_details.objects.create(
            book_id=book,
            member_id=member,
            status='Pending'
        )
        return redirect('view_book', id)
    else:
        # return redirect('view_book', id)
        return JsonResponse({'success': False, 'message': 'Book is not available.'})
    
    
    
def admin_issuebook(request):
    # x=Member.objects.select_related('member_id').filter(member_id__is_active=False)
    # borrow = Borrowing_details.objects.select_related('member_id').all()
    # borrow = Borrowing_details.objects.select_related('member_id').order_by('-id')
    borrow = Borrowing_details.objects.select_related('member_id').annotate(
    status_priority=Case(
        When(status='Pending', then=Value(1)),
        default=Value(2),
        output_field=IntegerField()
    )).order_by('status_priority', '-id')

    pending_reservations_count = Reservation.objects.filter(status='Pending').count()
    
    return render(request,'admin-issue-book.html',
                  {'borrow_request':borrow,
                   'pending_reservations_count': pending_reservations_count
                   })


def approve_borrow(request, id):

    borrow = get_object_or_404(Borrowing_details, id=id)
    borrow.status = 'Approved'
    borrow.approved = True
    borrow.approved_by = request.user
    borrow.approved_date = timezone.now()
    borrow.due_date = borrow.approved_date.date() + timezone.timedelta(days=14)  # Set due date (14 days later)
    borrow.save()
    
    # Reduce the available copies
    borrow.book_id.copies_available -= 1
    borrow.book_id.save()  # Save the updated book copies
    
    return redirect('admin_issuebook')



def reject_borrow(request, id):
    borrow = get_object_or_404(Borrowing_details, id=id)
    borrow.status = 'Rejected'
    borrow.save()
    return redirect('admin_issuebook')


def initiate_return_book(request, borrow_id):
    # borrowing = Borrowing_details.objects.filter(member_id=member, book_id=book).order_by('-id').first()

    borrowing = get_object_or_404(Borrowing_details, id=borrow_id)
    
    if borrowing.status == 'Approved':
        # Calculate fine before returning the book
        today = timezone.now().date()
        borrowing.days_overdue = (today - borrowing.due_date).days
        borrowing.calculate_fine()

    return render(request, 'member-return-book.html',{'borrow_details':borrowing})

  



@csrf_exempt
def create_razorpay_fine_order(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))  # Amount in paise
        currency = 'INR'
        receipt = 'order_rcptid_11'

        try:
            order = client.order.create({
                'amount': amount,
                'currency': currency,
                'receipt': receipt,
                'payment_capture': 1  # Auto-capture payment
            })
            return JsonResponse({'order_id': order['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def verify_fine_payment(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        book_name = request.POST.get('book_name')
        student_id = request.POST.get('student_id')
        fine_amount = int(request.POST.get('fine_amount')) / 100  # Convert back to rupees

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            # Payment is successful and verified

            # Fetch the member and book details
            member = get_object_or_404(Member, student_id=student_id)
            book = get_object_or_404(Book, title=book_name)

            # Ensure we update only unreturned records
            borrowing = Borrowing_details.objects.filter(
                book_id=book.id,
                member_id=member.id,
                returned=False  
            ).order_by('-id').first()
            
            # Save payment details to the database
            payment = Fine_Payment(
                name=book_name,
                member_id=member.id,
                book_id=book.id,
                borrow_id=borrowing,
                book_rate=fine_amount,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_status='success',
                razorpay_payment_id=razorpay_payment_id,
                paid=True
            )
            payment.save()
            
            # Update the Borrowing_details record
            
            if borrowing:
                borrowing.returned = True
                borrowing.returned_date = timezone.now().date()
                borrowing.status = 'Returned'
                borrowing.fine_paid = True
                borrowing.save()
                
                # Increment the available copies of the book
                book.copies_available += 1
                book.save()
            else:
                return JsonResponse({'status': 'error', 'message': 'No active borrowing record found'}, status=400)        
            

            return JsonResponse({'status': 'success'})
            # return redirect('view_book', book.id)
            
        except razorpay.errors.SignatureVerificationError:
            # Payment verification failed
            return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)
        except Exception as e:
            # Handle other exceptions
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



def return_book(request, borrow_id):
    if request.method == 'POST':

        borrowing = get_object_or_404(Borrowing_details, id=borrow_id)
        

        borrowing.returned = True
        borrowing.returned_date = timezone.now().date()
        borrowing.status = 'Returned'
        # borrowing.book_id.copies_available += 1
        borrowing.save()
        
        book = borrowing.book_id
        book.copies_available += 1
        book.save()
        
        return redirect('view_book', id=book.id)
        
    else:
        return redirect('view_book', id = book.id)
    
            
from django.core.mail import send_mail
  
def ForgotPassword(request):
    if request.method == "POST":
        
        email = request.POST.get('email')
        print(email)
          
        if User.objects.filter(email=email).exists():
            print('user exists')
            user = User.objects.get(email=email)
            
            send_mail("Reset Your Password: ", f"Hello {user}, \n\nYou requested a password reset for your account. Please click the link below to reset your password: \n \n \nhttp://127.0.0.1:8000/new_password/{user}/ ", settings.EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, 'A reset password link has been sent to your email.')
            return render(request, 'home-password-forgot.html')

            
        else:
            messages.error(request, 'Email not found.')
            return render(request, 'home-password-forgot.html')
    
    return render(request, 'home-password-forgot.html')
 

   
def RestNewPassword(request, user):
    # username = User.objects.get(username=user)
    try:
        # Get the user object
        user_obj = User.objects.get(username=user)
    except User.DoesNotExist:
        # If the user does not exist, show an error message
        messages.error(request, 'User not found.')
        return redirect('forgot_password')
    
    if request.method == "POST":
        pass1 = request.POST.get('new_password')
        pass2 = request.POST.get('confirm_password')
        
        print(pass1,pass2)
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'home-password-new.html', {'user': user_obj})
        
        user_obj.set_password(pass1)
        user_obj.save()
        
        # Show success message
        messages.success(request, 'Your password has been reset successfully.')
        return redirect(logins)
        
    return render(request, 'home-password-new.html')

# from django.shortcuts import render, redirect
# from django.contrib import messages
# import re

# def reset_password(request):
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')

#         # Password conditions
#         min_length = 8
#         has_upper = re.search(r'[A-Z]', new_password)
#         has_lower = re.search(r'[a-z]', new_password)
#         has_number = re.search(r'\d', new_password)
#         has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password)

#         # Validate password
#         if len(new_password) < min_length:
#             messages.error(request, 'Password must be at least 8 characters long.')
#         elif not has_upper:
#             messages.error(request, 'Password must contain at least one uppercase letter.')
#         elif not has_lower:
#             messages.error(request, 'Password must contain at least one lowercase letter.')
#         elif not has_number:
#             messages.error(request, 'Password must contain at least one number.')
#         elif not has_special:
#             messages.error(request, 'Password must contain at least one special character.')
#         elif new_password != confirm_password:
#             messages.error(request, 'Passwords do not match.')
#         else:
#             # Save the new password 
#             messages.success(request, 'Your password has been reset successfully.')
#             return redirect('login')  # Redirect to login page or another page

#     return render(request, 'reset_password.html') 


def admin_view_book(request):
    books = Book.objects.all()
    # books= Book.objects.select_related('title').all()

    # # Filter by genre if genre is provided
    # genre = request.GET.get('genre')
    # if genre:
    #     books = books.filter(genres=genre)

    # # Search by title or author if search query is provided
    # search_query = request.GET.get('search')
    # if search_query:
    #     books = books.filter(title__icontains=search_query) | books.filter(author__icontains=search_query)

    # # Get unique genres for the filter dropdown
    # genres = Book.objects.values_list('genres', flat=True).distinct()

    return render(request, 'admin-book-list.html', {'books': books})



def get_book_details(request, book_id):
    book = Book.objects.get(id=book_id)
    data = {
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'publication_date': book.publication_date,
        'genres': book.genres,
        'copies_available': book.copies_available,
        'description': book.description,
        'book_cover': book.book_cover.url if book.book_cover else ''
    }
    return JsonResponse(data)




@csrf_exempt
def update_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.isbn = request.POST.get('isbn')
        book.publication_date = request.POST.get('publication_date')
        book.genres = request.POST.get('genres')
        book.copies_available = request.POST.get('copies_available')
        book.description = request.POST.get('description')
        book.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def delete_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        book.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


from django.contrib.auth import update_session_auth_hash
@login_required
def ChangePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate old password
        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please enter it again.')
            return redirect('change_password')

        # Validate new password
        if new_password != confirm_password:
            messages.error(request, 'The new password and confirm password do not match.')
            return redirect('change_password')

        # Set new password
        request.user.set_password(new_password)
        request.user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password has been changed successfully.')
        return redirect('change_password')  # Redirect to profile or another page

    return render(request, 'admin-change-password.html')


    # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    # return render(request, 'admin-index_of_admin.html')
    
def borrowing_list(request):
    borrowings = Borrowing_details.objects.filter(approved=True).order_by('-id')
    # borrowings = Borrowing_details.objects.all().order_by('approved_date')
    today = now().date()
    return render(request, 'admin-borrowing-list.html', {'borrowings': borrowings, 'today':today})

def PurchasedBooksView(request):
    purchased_books = Payment.objects.filter(razorpay_payment_status="success")
    
    return render(request, 'admin-book-purchase.html', {'purchased_books': purchased_books})


def ReturnedBooksView(request):
    returned_books = Borrowing_details.objects.filter(returned = True).order_by('-returned_date')

    return render(request, 'admin-returned-book.html', {'returned_books': returned_books})

def admin_issued_book(request):
    
    issued_books = Borrowing_details.objects.filter(
        returned=False,
        status='Approved'
        ).order_by('-approved_date')
    
    today = timezone.now().date()
    for record in issued_books:
        record.days_overdue = (today - record.due_date).days
        record.calculate_fine()
    return render(request,'admin-issued-books.html',{'issued_books':issued_books} )


def admin_overdue(request):
    today = timezone.now().date()

    overdue_books = Borrowing_details.objects.filter(
        due_date__lt=today,
        returned=False
    ).order_by('due_date')
    
    for record in overdue_books:
        record.days_overdue = (today - record.due_date).days
        record.calculate_fine()
        
        
    return render(request, 'admin-overdue-books.html', 
                  {'overdue_books': overdue_books,})
    
def admin_mark_returned(request, book_id, member_id):
    try:
        borrow = Borrowing_details.objects.get(book_id_id=book_id, member_id_id=member_id, returned=False)
        borrow.returned = True
        borrow.returned_date = timezone.now()
        borrow.status = 'Returned'
        borrow.fine_paid = True
        borrow.save()
        
        book = borrow.book_id
        book.copies_available += 1
        book.save()
        
        messages.success(request, "Book marked as returned.")
    except Borrowing_details.DoesNotExist:
        messages.error(request, "Borrowing record not found.")
    
    return redirect('admin_overdue_books')  
    
    
def Librarian_Details(request):
    # lib = Librarian.objects.all()
    lib = Librarian.objects.select_related('librarian_id').all()
    
    return render(request, 'admin-librarian.html', {'librarians':lib})


def librarian_edit(request, librarian_id):
    try:
        librarian = Librarian.objects.select_related('librarian_id').get(id = librarian_id)
        data = {
            'id': librarian.id,
            'first_name': librarian.librarian_id.first_name,
            'last_name': librarian.librarian_id.last_name,
            'email': librarian.librarian_id.email,
            'phone': librarian.phone_number,
            'address': librarian.address,
            'join_date': librarian.librarian_id.date_joined.strftime("%Y-%m-%d"),
        }
        return JsonResponse(data)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Librarian not found'}, status=404)
    


@csrf_exempt
def update_librarian(request, librarian_id):
    if request.method == 'POST':
        
        lib = Librarian.objects.get(id=librarian_id)
        user = lib.librarian_id
            
        # Update User 
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
            
        # Update Librarian
        
        lib.phone_number = request.POST.get('phone')
        lib.address = request.POST.get('address')
        lib.save()
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)




def librarian_status(request, librarian_id):
    lib = get_object_or_404(Librarian, id=librarian_id)
    
    # Toggle status (True becomes False, False becomes True)
    lib.status = not lib.status
    lib.save()
    
    return redirect('librarian')


# def delete_librarian(request,librarian_id):
#     lib = Librarian.objects.get(id=librarian_id)
#     user_id = lib.librarian_id.librarian_id
#     lib.delete()
#     User.objects.filter(id=user_id).delete()
#     return redirect(student_request)


def delete_librarian(request, librarian_id):
    try:
        lib = Librarian.objects.get(id=librarian_id)
        user = lib.librarian_id
        
        # Delete both librarian profile and user account
        lib.delete()
        user.delete()
        
        return JsonResponse({'status': 'success'})
    except Librarian.DoesNotExist:
        return JsonResponse({'error': 'Librarian not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
def member_profile(request):
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    user = User.objects.get(id=memb)
    return render(request, 'member-profile-view.html',{'view':member,'data':user})
    # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    # return render(request, 'admin-starter-page.html')
    # return render(request, 'admin_home_front.html')
    # return render(request, 'index.html')
    # return render(request, 'starter-page.html')
    # return render(request, 'home.html')
    
    
def member_profile_edit(request):
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    user = User.objects.get(id=memb)
    return render(request,'member-profile-edit.html',{'view':member,'data':user})

def member_profile_update(request):
    if request.method=='POST':
    
        memb = request.session.get('stud_id')
        
        if not memb:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('logins')
        
        member = Member.objects.get(member_id_id=memb)
        user = User.objects.get(id=memb)
        
        if not request.POST['first_name']:
            messages.warning(request, 'First name is required.')
            return redirect('memberprofileedit')
        
        if not request.POST['email']:
            messages.warning(request, 'Email is required.')
            return redirect('memberprofileedit')

        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST['email']
        user.save()
        
        if 'profile_picture' in request.FILES:
            member.profile_picture = request.FILES['profile_picture']
                
        member.phone_number =request.POST['phone_number']
        member.address = request.POST['address']
        member.department = request.POST['department']
        member.year_of_study = request.POST['year']
        member.save()
        
        # return redirect('memberprofile')
        messages.success(request, 'Profile updated successfully!')
        return redirect('memberprofile')
    
    messages.success(request, 'Profile failed to update!')
    return redirect('memberprofile')


def add_to_wishlist(request, book_id):
    
    book = Book.objects.get(id=book_id)
    
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    
    saved = Wishlist.objects.create(member_id=member, book_id=book)
    saved.save
    return redirect('view_book', id = book_id)

def remove_from_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    
    Wishlist.objects.filter(member_id=member, book_id=book).delete()
    return redirect('view_book', id = book_id)


def view_wishlist(request):
    books = Wishlist.objects.all()
    return render(request, 'member-wishlist.html', {'books': books})

def remove_from_mywishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    
    Wishlist.objects.filter(member_id=member, book_id=book).delete()
    return redirect('member_view_wishlist')

def view_ebook(request):
    books = Payment.objects.all()
    return render(request, 'member-ebook.html', {'books': books})


def request_reservation(request, book_id):
    
    book = Book.objects.get(id=book_id)
    
    member_id = request.session.get('stud_id')
    member = get_object_or_404(Member, member_id_id=member_id)
    
    existing = Reservation.objects.filter(book_id=book, member_id=member, status='Pending')
    
    if existing:
        messages.warning(request, "You have already requested this book.")
    
    else:
        Reservation.objects.create(
            book_id=book,
            book_title=book.title,
            member_id=member,
            status='Pending',
            reservation_date=timezone.now()
        )
        messages.success(request, "Reservation request submitted successfully!")

    return redirect('view_book', id = book_id)
    


def view_reservaton(request):
    reservations = Reservation.objects.filter(
        status='Pending'
    ).order_by( 'book_title', 'reservation_date')
    return render(request, 'admin-book-reservation.html', {'reservations': reservations})


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = 'Cancelled'
    reservation.save()
    messages.warning(request, "Reservation rejected!")
    return redirect('view_reservation')

def approve_reservation(request, reservation_id):
    
      
    reserve = Reservation.objects.get(id=reservation_id)
    book = reserve.book_id
    
    if book.copies_available > 0:
        
        borrow =Borrowing_details.objects.create(
            book_id=reserve.book_id,
            member_id=reserve.member_id,
            status = 'Approved',
            approved = True,
            approved_by = request.user,
            approved_date = timezone.now(),
            due_date = timezone.now().date() + timezone.timedelta(days=14),
            
        )
        borrow.save()

        book.copies_available -=1
        book.save()
    
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.status = 'Approved'
        reservation.save()
        messages.success(request, "Reservation approved and book borrowed successfully.")
    else:
        messages.warning(request, "No copies available to approve this reservation.")

    
    return redirect('view_reservation')



def member_changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
         # Validate old password
        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please enter it again.')
            return redirect('member_changepassword')

        # Validate new password
        if new_password != confirm_password:
            # messages.error(request, 'The new password and confirm password do not match.')
            return redirect('member_changepassword')

        # Set new password
        request.user.set_password(new_password)
        request.user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password has been changed successfully.')
        return redirect('memberprofile')  # Redirect to profile or another page

         
    return render(request, 'member-change-password.html')


def view_member_fine(request):
    member_id = request.session.get('stud_id')
    member = get_object_or_404(Member, member_id_id=member_id)
    
    today = timezone.now().date()

    overdue_books = Borrowing_details.objects.filter(
        member_id=member,
        due_date__lt=today,
        returned=False
        )
    
    for record in overdue_books:
        record.days_overdue = (today - record.due_date).days
        record.calculate_fine()
        
    return render(request, 'member-book-fine.html',{'books':overdue_books})


def member_issued_books(request):
    member_id = request.session.get('stud_id')
    member = get_object_or_404(Member, member_id_id=member_id)
    
    issued_books = Borrowing_details.objects.filter(
        member_id=member,
        # due_date__gt=today,
        returned=False,
        status='Approved'
        ).order_by('-approved_date')
    
    today = timezone.now().date()
    for record in issued_books:
        record.days_overdue = (today - record.due_date).days
        record.calculate_fine()
        
    return render(request, 'member-issued-book.html',{'books':issued_books})



def member_borrow_details(request):
    member_id = request.session.get('stud_id')
    member = get_object_or_404(Member, member_id_id=member_id)
    
    books = Borrowing_details.objects.filter(
        member_id=member
        ).select_related('book_id').order_by('-id')
    
    
    for record in books:
        record.calculate_fine()
        
    return render(request, 'member-borrow-details.html',{'books':books, 'today': timezone.now().date()})




def member_book_reservations(request):
    member_id = request.session.get('stud_id')
    member = get_object_or_404(Member, member_id_id=member_id)
    
    reservations = Reservation.objects.filter(
        member_id=member).select_related('book_id').order_by('-reservation_date')
    
    return render(request, 'member-book-reservation.html', {'reservations': reservations})



def member_cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = 'Cancelled'
    reservation.save()
    messages.warning(request, "Reservation Cancelled!")
    return redirect('mybook_reservations')

from django.db.models import Sum

def librarian_homepage(request):
    lib = request.session.get('lib_id')
    librarian = Librarian.objects.get(librarian_id_id=lib)
    user = User.objects.get(id=lib)
 
    total_books_count = Book.objects.all().count()
    new_requests_count = User.objects.filter(is_active=0).count()
    # stock_books_count = Book.objects.filter(copies_available__gt = 0).count()
    issue_count = Borrowing_details.objects.filter(status = "Pending").count()
    
    # issued_books_count = Borrowing_details.objects.filter(status='Approved').count()
    overdue_count = Borrowing_details.objects.filter(due_date__lt=timezone.now().date(), returned_date__isnull=True).count()
    active_count = Member.objects.filter(status=True).count()
    overdue_books_sum = Borrowing_details.objects.filter(due_date__lt=timezone.now().date(),returned_date__isnull=True).aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    
    books = Borrowing_details.objects.filter(
        due_date__lt=timezone.now().date()
        ).select_related('book_id').order_by('-id')
    
    
    for record in books:
        record.calculate_fine()
    
  
    
    context = {
        'total': total_books_count,
        'requests' : new_requests_count,
        'issued': issue_count,
        'overdue': overdue_count,
        'active': active_count,
        'total_fine':overdue_books_sum
    }
    return render(request, 'librarian-home-page.html',context)
    
    

def librarian_profile(request):
    lib = request.session.get('lib_id')
    librarian = Librarian.objects.get(librarian_id_id=lib)
    user = User.objects.get(id=lib)
    return render(request, 'librarian-profile-view.html',{'view':librarian,'data':user})

    
    
def librarian_profile_edit(request):
    lib = request.session.get('lib_id')
    librarian = Librarian.objects.get(librarian_id_id=lib)
    user = User.objects.get(id=lib)
    return render(request,'librarian-profile-edit.html',{'view':librarian,'data':user})

def librarian_profile_update(request):
    if request.method=='POST':
    
        lib = request.session.get('lib_id')

        
        if not lib:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('logins')
        
        librarian = Librarian.objects.get(librarian_id_id=lib)
        user = User.objects.get(id=lib)
        
        if not request.POST['first_name']:
            messages.warning(request, 'First name is required.')
            return redirect('memberprofileedit')
        
        if not request.POST['email']:
            messages.warning(request, 'Email is required.')
            return redirect('memberprofileedit')

        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST['email']
        user.save()
        
        if 'profile_picture' in request.FILES:
            librarian.profile_picture = request.FILES['profile_picture']
                
        librarian.phone_number =request.POST['phone_number']
        librarian.address = request.POST['address']

        librarian.save()
        
        # return redirect('memberprofile')
        messages.success(request, 'Profile updated successfully!')
        return redirect('librarianprofile')
    
    messages.success(request, 'Profile failed to update!')
    return redirect('librarianprofile')

def librarian_changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
         # Validate old password
        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please enter it again.')
            return redirect('librarian_changepassword')

        # Validate new password
        if new_password != confirm_password:
            # messages.error(request, 'The new password and confirm password do not match.')
            return redirect('librarian_changepassword')

        # Set new password
        request.user.set_password(new_password)
        request.user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password has been changed successfully.')
        return redirect('librarianprofile')  # Redirect to profile or another page

         
    return render(request, 'librarian-change-password.html')


def librarian_view_book(request):
    books = Book.objects.all()
 
    return render(request, 'librarian-book-list.html', {'books': books})

def librarian_student_request(request):

    mem = Member.objects.order_by('member_id__is_active', '-id')

    return render(request,'librarian-student-request.html',{'student_req':mem})

def librarian_approve_student(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    
    stud.member_id.is_active = True
    stud.member_id.save()
    return redirect('librarian_student_request')


def librarian_delete_student(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    user_id = stud.member_id.id
    stud.delete()
    User.objects.filter(id=user_id).delete()
    return redirect('librarian_student_request')


def librarian_view_studentlist(request):
    students = Member.objects.select_related('member_id').filter(member_id__is_active=True)
    return render(request,'librarian-studentlist.html',{'student_list':students})

def librarian_delete_member(request,id):
    stud = Member.objects.get(id=id)
    user_id = stud.member_id.id
    stud.delete()
    User.objects.filter(id=user_id).delete()
    return redirect('librarian_view_studentlist')


def librarian_activate_member(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    stud.status = True
    stud.save()
    return redirect('librarian_view_studentlist')

def librarian_deactivate_member(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    stud.status = False
    stud.save()
    return redirect('librarian_view_studentlist')


def librarian_add_members(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']  
        username = request.POST['username']  
        password  = request.POST['password']
        confirm_password  = request.POST['confirm_password']   
        email  = request.POST['email']   
        phone = request.POST['phone']  
        student_id  = request.POST['student_id']  
        department  = request.POST['department']  
        year  = request.POST['year']
        image = request.FILES.get('profile_picture')
        address = request.POST['address']    
        
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                        'status': 'error',
                        'message': 'Username is already taken.'
                    }, status=400)
            # messages.error(request, "Username already exists. Please choose another!")
            # return redirect('librarian_add_member')
        #     # messages.error(request, "Username is already taken.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Username is already taken');window.location.href='http://127.0.0.1:8000/adminaddmembers/script>")
           
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                        'status': 'error',
                        'message': 'Email is already registered.'
                    }, status=400)
            # messages.error(request, "Email already exists. Please use another email!")
            # return redirect('librarian_add_member')
        #    return HttpResponse("<script>alert('Email is already taken');window.location.href='http://127.0.0.1:8000/adminaddmembers/';</script>")
           
           
        if password != confirm_password:
            return JsonResponse({
                        'status': 'error',
                        'message': 'Passwords do not match.'
                    }, status=400)
            # messages.error(request, "Passwords do not match.")
            # return redirect('index_of_home')
            # messages.error(request, "Passwords do not match!")
            # return redirect('librarian_add_member')
            # return HttpResponse("<script>alert('Password do not match');window.location.href='http://127.0.0.1:8000/adminaddmembers/';</script>")
            
        if Member.objects.filter(student_id=student_id).exists():
            messages.error(request, "Student ID already exists.!")
            return redirect('librarian_add_member')
       
              
        try:    
            user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email, usertype='Student',is_active=True,is_staff=False)
            user.save()
            
            member=Member.objects.create(member_id=user, student_id = student_id, year_of_study = year, department = department, phone_number=phone,address=address, status=True, profile_picture = image)
            member.save()
            # messages.success(request, "Student added successfully!")
            # return redirect('librarian_add_member')
            return JsonResponse({
                'status': 'success',
                'message': 'Student added successfully!'
            })
        
        
        except Exception as e:
             return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=500)
            # Return error response
            # messages.error(request, f"Error: {str(e)}")
            # return redirect('librarian_add_member')
        
        # return HttpResponse("<script>alert('Request for Registration Completed');window.location.href='http://127.0.0.1:8000/studentlist/';</script>")
                
    else:    
    
        return render(request, 'librarian-add-student.html')
    
    
def librarian_issuebook(request):

    # borrow = Borrowing_details.objects.select_related('member_id').order_by('-id')
    borrow = Borrowing_details.objects.select_related('member_id').annotate(
    status_priority=Case(
        When(status='Pending', then=Value(1)),
        default=Value(2),
        output_field=IntegerField()
    )
).order_by('status_priority', '-id')
    
    pending_reservations_count = Reservation.objects.filter(status='Pending').count()

    return render(request,'librarian-issue-books.html',
                  {'borrow_request':borrow,
                   'pending_reservations_count': pending_reservations_count
                   })
 

def librarian_approve_borrow(request, id):

    borrow = get_object_or_404(Borrowing_details, id=id)
    borrow.status = 'Approved'
    borrow.approved = True
    borrow.approved_by = request.user
    borrow.approved_date = timezone.now()
    borrow.due_date = borrow.approved_date.date() + timezone.timedelta(days=14)  # Set due date (14 days later)
    borrow.save()
    
    # Reduce the available copies
    borrow.book_id.copies_available -= 1
    borrow.book_id.save()  # Save the updated book copies
    
    return redirect('librarian_issuebook')

def librarian_reject_borrow(request, id):
    borrow = get_object_or_404(Borrowing_details, id=id)
    borrow.status = 'Rejected'
    borrow.save()
    return redirect('librarian_issuebook')


def librarian_view_reservaton(request):
    reservations = Reservation.objects.filter(
        status='Pending'
    ).order_by( 'book_title', 'reservation_date')
    return render(request, 'librarian-book-reservation.html', {'reservations': reservations})


def librarian_cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = 'Cancelled'
    reservation.save()
    messages.info(request, "Reservation rejected!")
    return redirect('librarian_view_reservation')


def librarian_approve_reservation(request, reservation_id):
    
      
    reserve = Reservation.objects.get(id=reservation_id)
    book = reserve.book_id
    
    if book.copies_available > 0:
        
        borrow =Borrowing_details.objects.create(
            book_id=reserve.book_id,
            member_id=reserve.member_id,
            status = 'Approved',
            approved = True,
            approved_by = request.user,
            approved_date = timezone.now(),
            due_date = timezone.now().date() + timezone.timedelta(days=14),
            
        )
        borrow.save()

        book.copies_available -=1
        book.save()
    
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.status = 'Approved'
        reservation.save()
        messages.success(request, "Reservation approved and book borrowed successfully.")
    else:
        messages.warning(request, "No copies available to approve this reservation.")

    
    return redirect('librarian_view_reservation')


def librarian_add_book(request):
    if request.method == "POST":
        try:
            title = request.POST['title']
            author = request.POST['author']
            isbn = request.POST['isbn']
            publish = request.POST['publication_date']
            b_cover = request.FILES.get('cover')
            book = request.FILES.get('book')
            genre = request.POST['genre']
            copies = request.POST['copies']
            about = request.POST['description']
            price = request.POST['price']
        
        
            if Book.objects.filter(title=title).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'A book with this Title already exists.'
                }, status=400)
                
            if Book.objects.filter(isbn=isbn).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'A book with this ISBN already exists.'
                }, status=400)
        
        
            # Create and save the book
            book = Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                publication_date=publish,
                book_cover=b_cover,
                book_upload=book,
                genres=genre,
                copies_available=copies,
                description=about,
                rate=price
            )
            book.save()
            
            # return HttpResponse('success:Book added successfully!')
            # messages.success(request, "Book added successfully!")
            # return redirect('librarian_add_book')
            return JsonResponse({
                'status': 'success',
                'message': 'Book added successfully!',
                'book_id': book.id
            })
        except Exception as e:
            # messages.error(request, f"Error: {str(e)}")
            # return redirect('add_book')
            return JsonResponse({
                'status': 'error',
                'message': f'Error adding book: {str(e)}'
            }, status=500)
           
    else:
        return render(request, 'librarian-add-book.html')
        


def librarian_overdue(request):
    today = timezone.now().date()

    overdue_books = Borrowing_details.objects.filter(
        due_date__lt=today,
        returned=False
    ).order_by('due_date')
    
    for record in overdue_books:
        record.days_overdue = (today - record.due_date).days
        record.calculate_fine()
        
        
    return render(request, 'librarian-overdue-books.html', 
                  {'overdue_books': overdue_books,})
    

def librarian_mark_returned(request, book_id, member_id):
    try:
        borrow = Borrowing_details.objects.get(book_id_id=book_id, member_id_id=member_id, returned=False)
        borrow.returned = True
        borrow.returned_date = timezone.now()
        borrow.status = 'Returned'
        borrow.fine_paid = True
        borrow.save()
        
        book = borrow.book_id
        book.copies_available += 1
        book.save()
        
        messages.success(request, "Book marked as returned.")
    except Borrowing_details.DoesNotExist:
        messages.error(request, "Borrowing record not found.")
    
    return redirect('librarian_overdue_books')  


def librarian_fine_list(request):
    today = timezone.now().date()

    fine_books = Borrowing_details.objects.filter(
        due_date__lt=today
    ).order_by('fine_paid', 'due_date')
    
    for record in fine_books:
        record.days_overdue = (today - record.due_date).days
        record.calculate_fine()
        record.payment = Fine_Payment.objects.filter(borrow_id=record).first()
        
    overdue_books_sum = Borrowing_details.objects.filter(due_date__lt=timezone.now().date(),returned_date__isnull=True).aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    paid_books_sum = Borrowing_details.objects.filter(due_date__lt=timezone.now().date(),returned_date__isnull=False).aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    
  
    return render(request, 'librarian-finelist.html',
                  {'fine_books': fine_books,
                   'overdue': overdue_books_sum,
                   'paid': paid_books_sum})
    
    
def librarian_issued_book(request):
    
    issued_books = Borrowing_details.objects.filter(
        returned=False,
        status='Approved'
        ).order_by('-approved_date')
    
    today = timezone.now().date()
    for record in issued_books:
        record.days_overdue = (today - record.due_date).days
        record.calculate_fine()
    return render(request,'librarian-issued-books.html',{'issued_books':issued_books} )


def librarian_returned_booksView(request):
    returned_books = Borrowing_details.objects.filter(returned = True).order_by('-returned_date')

    return render(request, 'librarian-returned-books.html', {'returned_books': returned_books})


def librarian_borrowing_list(request):
    borrowings = Borrowing_details.objects.filter(approved=True).order_by('-id')
    # borrowings = Borrowing_details.objects.all().order_by('approved_date')
    today = now().date()
    return render(request, 'librarian-borrowing-list.html', {'borrowings': borrowings, 'today':today})

def librarian_purchased_books(request):
    purchased_books = Payment.objects.filter(razorpay_payment_status="success")
    
    return render(request, 'librarian-book-purchase.html', {'purchased_books': purchased_books})