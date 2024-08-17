from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Member, Book, Librarian
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

# Create your views here.


# def home(request):
#     return render(request, 'index_of_home.html')

# def login(request):
#     return render(request, 'login.html')

User = get_user_model()

# def Index(request):
#     return render(request, "login.html")

def member_reg(request):
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
            return HttpResponse("<script>alert('Password do not match');window.location.href='http://127.0.0.1:8000/#register';</script>")
            

        # if User.objects.filter(username=username).exists():
        #     # messages.error(request, "Username is already taken.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Username is already taken');window.location.href='http://127.0.0.1:8000/';</script>")
            

        # if User.objects.filter(email=email).exists():
        #     # messages.error(request, "Email is already registered.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Email is already taken');window.location.href='http://127.0.0.1:8000/';</script>")
            
            
        user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email, usertype='student',is_active=False,is_staff=False)
        user.save()
        
        member=Member.objects.create(member_id=user, student_id = student_id, year_of_study = year, department = department, phone_number=phone,address=address, profile_picture = image)
        member.save()
        
        return HttpResponse("<script>alert('Request for Registration Completed');window.location.href='http://127.0.0.1:8000/';</script>")
                
    else:
        return render(request,'index_of_home.html')
        
        
        
def logins(request):
    if request.method=='POST':
        USERNAME=request.POST['username']
        PASSWORD=request.POST['password']
        print(USERNAME)
        print(PASSWORD)
        userpass = authenticate(request, username=USERNAME, password=PASSWORD)
        if userpass is not None and userpass.is_superuser==1:
            print('admin')
            return redirect(admin_home)
            # return HttpResponse("<script>window.location.href='http://127.0.0.1:8000/home/homepage/';</script>")
            
        
        elif userpass is not None and userpass.is_staff==1:
            print('librarian')
            login(request, userpass)
            request.session['lib_id']=userpass.id
            return redirect(librarian_homepage)
        
        elif userpass is not None and userpass.is_active==1:
            print('member')
            login(request, userpass)
            request.session['stud_id']=userpass.id
            return redirect(member_homepage)
        
        # elif userpass is not None and not userpass.is_active:
        #     print('pending request')
        #     # login(request, userpass)
        #     return HttpResponse("<script>alert('Your account is pending approval.');window.location.href='http://127.0.0.1:8000/login';</script>")
            
        #     return render(request, 'login.html', {'error': 'Your account is pending approval.'})
        
        else:
            # return HttpResponse('Invalid Login')
            return HttpResponse("<script>alert('Username or Password doesnot exist!');window.location.href='http://127.0.0.1:8000/login';</script>")
            
        
    else:
        return render(request, 'login.html')
 

def logouts(request):
    logout(request)
    return redirect(logins)        

def admin_home(request):
    # return HttpResponse("Welcome")
    # return render(request, 'admin-starter-page.html')
    # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    return render(request, 'admin_home.html')
    # return render(request, 'admin-index_of_admin.html')
    
def view_studentlist(request):
    x=Member.objects.select_related('member_id').filter(member_id__is_active=True)
    return render(request,'studentlist.html',{'student_list':x})


def student_request(request):
    # x=Member.objects.select_related('member_id').filter(member_id__is_active=False)
    mem=Member.objects.select_related('member_id').all()
    return render(request,'studentrequest.html',{'student_req':mem})


def admin_approve_student(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    
    stud.member_id.is_active = True
    stud.member_id.save()
    return redirect(student_request)

def admin_delete_student(request,id):
    stud = Member.objects.get(id=id)
    user_id = stud.member_id.id
    stud.delete()
    User.objects.filter(id=user_id).delete()
    return redirect(student_request)

def admin_delete_member(request,id):
    stud = Member.objects.get(id=id)
    user_id = stud.member_id.id
    stud.delete()
    User.objects.filter(id=user_id).delete()
    return redirect(view_studentlist)


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
            return HttpResponse("<script>alert('Password do not match');window.location.href='http://127.0.0.1:8000/adminaddmembers/';</script>")
            

        # if User.objects.filter(username=username).exists():
        #     # messages.error(request, "Username is already taken.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Username is already taken');window.location.href='http://127.0.0.1:8000/adminaddmembers/script>")
            

        # if User.objects.filter(email=email).exists():
        #     # messages.error(request, "Email is already registered.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Email is already taken');window.location.href='http://127.0.0.1:8000/adminaddmembers/';</script>")
            
            
        user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email, usertype='Student',is_active=True,is_staff=False)
        user.save()
        
        member=Member.objects.create(member_id=user, student_id = student_id, year_of_study = year, department = department, phone_number=phone,address=address, profile_picture = image)
        member.save()
        
        return HttpResponse("<script>alert('Request for Registration Completed');window.location.href='http://127.0.0.1:8000/studentlist/';</script>")
                
    else:    
    
        return render(request, 'admin-add-student.html')



def admin_activate_member(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    stud.status = True
    stud.save()
    return redirect(view_studentlist)

def admin_deactivate_member(request,id):
    print(id)
    stud = Member.objects.get(id=id)
    stud.status = False
    stud.save()
    return redirect(view_studentlist)


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
        
        book = Book.objects.create(title = title, author = author, isbn = isbn, publication_date = publish, book_cover = b_cover, book_upload = book, genres = genre, copies_available = copies, description = about )
        book.save()
        
        return HttpResponse("<script>alert('Book Addeed Successfully');window.location.href='http://127.0.0.1:8000/homepage/';</script>")
        
    else:
        return render(request, 'admin-addbook.html')
    # return render(request, 'admin-service-details.html')
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
            return HttpResponse("<script>alert('Password do not match');window.location.href='http://127.0.0.1:8000/adminaddlibrarian/';</script>")
            

        # if User.objects.filter(username=username).exists():
        #     # messages.error(request, "Username is already taken.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Username is already taken');window.location.href='http://127.0.0.1:8000/adminaddlibrarian/script>")
            

        # if User.objects.filter(email=email).exists():
        #     # messages.error(request, "Email is already registered.")
        #     # return redirect('index_of_home')
        #     return HttpResponse("<script>alert('Email is already taken');window.location.href='http://127.0.0.1:8000/adminaddlibrarian/';</script>")
            
            
        user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email, usertype='Librarian',is_active=True,is_staff=True)
        user.save()
        
        lib=Librarian.objects.create(librarian_id=user, phone_number=phone,address=address, profile_picture = image)
        lib.save()
        
        return HttpResponse("<script>alert('Librarian Added');window.location.href='http://127.0.0.1:8000/homepage/';</script>")
                
    else:    
    
        return render(request, "admin-add-librarian.html")
    
    
def member_homepage(request):
    memb = request.session.get('stud_id')
    member = Member.objects.get(member_id_id=memb)
    user = User.objects.get(id=memb)
    return render(request, 'member-home_page.html',{'view':member,'data':user})
    # return render(request, 'index.html')
    # return render(request, 'starter-page.html')
    
    # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    # return render(request, 'admin-index_of_admin.html')

def librarian_homepage(request):
    lib = request.session.get('lib_id')
    librarian = Librarian.objects.get(librarian_id_id=lib)
    user = User.objects.get(id=lib)
    # return render(request, 'member-home_page.html',{'view':librarian,'data':user})
    return render(request, 'admin-starter-page.html')
    # return render(request, 'admin-service-details.html')
    # return render(request, 'admin-portfolio-detail.html')
    # return render(request, 'admin-index_of_admin.html')
    
    
def search_book(request):
    if request.method == "POST":
        search = request.POST['search']
        print(search,"pppppppppp")
        
        if search:
            book = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search) | Book.objects.filter(isbn__icontains=search)
        else:
            book = Book.objects.none()
                    
        return render(request, 'member-search-result.html', {'results': book, 'search':search})
    else:
        return render(request, 'member-home_page.html')
    
    
def view_book(request,id):
    print(id)
    book = Book.objects.get(id=id)
    
    return render(request,"book-view.html", {'book' : book} )










