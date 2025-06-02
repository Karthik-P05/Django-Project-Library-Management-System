"""
URL configuration for LibraryManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views

from django.conf import settings
from django.conf.urls.static import static
# from adminapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # path('', include('home.urls')),
    
    # path('home/', include('adminhomepage.urls')),
    
    path('', views.member_reg, name='homepage'),
    
    path('memberregistration/', views.member_reg, name='member_registration'),
    
    path('login/', views.logins, name='logins'),
    
    path('homepage/', views.admin_home, name='admin_homepage'),
    
    path('logouts/',views.logouts, name='logout'),
    
    path('studentlist/',views.view_studentlist, name='view_studentlist'),
    
    # path('studentlist/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    
    path('studentlist/<int:member_id>/edit/', views.edit_student, name='edit_member'),
    
    path('studentlist/update/<int:member_id>/', views.update_member, name='update_member'),
       
    path('admindeletemember/<int:id>',views.admin_delete_member, name='admin_delete_member'),
    
    # path('members/update/', views.update_member, name='update_member'),
    
    path('studentrequest/', views.student_request, name='student_request'),
    
    path('adminapprovestudent/<int:id>',views.admin_approve_student, name='admin_approve_student'),
    
    path('admindeletestudent/<int:id>',views.admin_delete_student, name='admin_adelete_student'),
    
    # path('adminviewmember/<int:id>', views.admin_view_member),
    
    path('adminaddmembers/', views.admin_add_members, name='add_member'),
    
    path('adminactivatemember/<int:id>',views.admin_activate_member),
    
    path('admindeactivatemember/<int:id>',views.admin_deactivate_member),
    
    path('addbook', views.add_book, name='add_book'),  
    
    path('adminaddlibrarian', views.admin_add_librarian, name='add_librarian'),
    
    path('memberhomepage/', views.member_homepage, name='member_homepage'),
    
    path('librarianhomepage/', views.librarian_homepage, name='librarian_homepage'),
    
    path('searchresult/', views.search_book, name='search_book'),
    
    path('viewbook/<int:id>', views.view_book, name='view_book'),
    
    path('ebook/<int:id>', views.checkout_ebook, name='checkout_ebook'),
    
    # path('ebookpayment/', views.ebook_payment),
    
    path('create_razorpay_order/', views.create_razorpay_order, name='create_razorpay_order'),
    
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    
    path("view_pdf/<int:id>", views.view_pdf, name="view_pdf"),
    
    path("book_review/", views.review_and_rating,  name="submit_review"),
    
    path('request_borrow/<int:id>/', views.borrow_request, name='request_borrow'),
    
    path('admin_issuebook/', views.admin_issuebook, name='admin_issuebook'),
    
    path('admin_issuedbooks/', views.admin_issued_book, name='admin_issued_books'),
    
    path('admin_overdue_books/', views.admin_overdue, name='admin_overdue_books'),
    
    path('adminreturnbook/<int:book_id>/<int:member_id>/', views.admin_mark_returned, name='admin_mark_returned'),
    
    path('approve_borrow/<int:id>/', views.approve_borrow, name='approve_borrow'),
    
    path('reject_borrow/<int:id>/', views.reject_borrow, name='reject_borrow'),
    
    path('check-return-book/<int:borrow_id>/', views.initiate_return_book, name='initiate_return_book'),
      
    path('create_razorpay_fine_order/', views.create_razorpay_fine_order, name='create_razorpay_fine_order'),
    
    path('verify_fine_payment/', views.verify_fine_payment, name='verify_fine_payment'),
    
    path('return-book/<int:borrow_id>/', views.return_book, name='return_book'),
    
    path('forgot-password/', views.ForgotPassword, name='ForgotPassword'),
    
    path('new_password/<str:user>/', views.RestNewPassword, name='Rest_password'),
    
    path('book_list/', views.admin_view_book, name='book_list'),

    path('get-book-details/<int:book_id>/', views.get_book_details, name='get_book_details'),
    
    path('update-book/<int:book_id>/', views.update_book, name='update_book'),
    
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
    
    path('change_password/', views.ChangePassword, name='change_password'),
    
    path('borrowing_list/', views.borrowing_list, name='borrowing_list'),
    
    path('puchased_books/', views.PurchasedBooksView, name='purchased_books'),
    
    path('returned_books/', views.ReturnedBooksView, name='returned_books'),
    
    path('librarian/', views.Librarian_Details, name='librarian'),
    
    path('librarians/<int:librarian_id>/edit/', views.librarian_edit, name='edit_librarian'),
    
    path('librarians/<int:librarian_id>/update/', views.update_librarian, name='update_librarian'),
    
    path('librarians/<int:librarian_id>/status/', views.librarian_status, name='librarian_status'),
    
    path('librarians/<int:librarian_id>/delete/', views.delete_librarian, name='delete_librarian'),
     
    
    path('memberprofile/', views.member_profile, name='memberprofile'),
    
    path('memberprofileedit/', views.member_profile_edit, name='memberprofileedit'),
    
    path('memberprofileupdate/', views.member_profile_update, name='memberprofileupdate'),
    
    
    path('addwishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    path('removewishlist/<int:book_id>/', views.remove_from_wishlist, name='remove_wishlist'),
    
    path('memberviewwishlist/', views.view_wishlist, name='member_view_wishlist'),
    
    path('memberebook/', views.view_ebook, name='member_ebook'),
    
    
    path('bookreserve/<int:book_id>/', views.request_reservation, name='send_reservation'),

    path('viewreservation/', views.view_reservaton, name='view_reservation'),
    
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    
    path('approve_reservation/<int:reservation_id>/', views.approve_reservation, name='approve_reservation'),
    
    path('memberchangepassword/', views.member_changepassword, name='member_changepassword'),
    
    path('removemywishlist/<int:book_id>/', views.remove_from_mywishlist, name='remove_mywishlist'),
    
    path('viewfinepayment/', views.view_member_fine, name='viewfinepayment'),
    
    path('viewissuedbook', views.member_issued_books, name='issued_book'),
    
    path('viewborrowingdetails/', views.member_borrow_details, name='borrow_details'),
    
    path('viewreservations/', views.member_book_reservations, name='mybook_reservations'),
    
    path('cancel_myreservation/<int:reservation_id>/', views.member_cancel_reservation, name='cancel_myreservation'),
    
    
    path('librarianprofile/', views.librarian_profile, name='librarianprofile'),
    
    path('librarianprofileedit/', views.librarian_profile_edit, name='librarianprofileedit'),
    
    path('librarianprofileupdate/', views.librarian_profile_update, name='librarianprofileupdate'),
    
    path('librarianchangepassword/', views.librarian_changepassword, name='librarian_changepassword'),
    
    path('librarianbooklist/', views.librarian_view_book, name='librarianbooklist'),
    
    path('librarianstudentrequest/', views.librarian_student_request, name='librarian_student_request'),
    
    path('librarianapprovestudent/<int:id>',views.librarian_approve_student, name='librarian_approve_student'),
    
    path('librariandeletestudent/<int:id>', views.librarian_delete_student, name='librariandeletestudent'),
    
    path('librarianstudentlist/',views.librarian_view_studentlist, name='librarian_view_studentlist'),
    
    path('librarianstudentlist/<int:member_id>/edit/', views.edit_student, name='librarian_edit_member'),
    
    path('librarianstudentlist/update/<int:member_id>/', views.update_member, name='librarian_update_member'),
       
    path('librariandeletemember/<int:id>',views.librarian_delete_member, name='librarian_delete_member'),
    
    path('librarianactivatemember/<int:id>',views.librarian_activate_member, name='librarian_activate_member'),
    
    path('librariandeactivatemember/<int:id>',views.librarian_deactivate_member, name='librarian_deactivate_member'),
    
    path('librarianaddmembers/', views.librarian_add_members, name='librarian_add_member'),
    
    path('librarianissuebook/', views.librarian_issuebook, name='librarian_issuebook'),
    
    path('librarianapproveborrow/<int:id>/', views.librarian_approve_borrow, name='librarian_approve_borrow'),
    
    path('librarianrejectborrow/<int:id>/', views.librarian_reject_borrow, name='librarian_reject_borrow'),

    path('librarianviewreservation/', views.librarian_view_reservaton, name='librarian_view_reservation'),
    
    path('librarian_cancel_reservation/<int:reservation_id>/', views.librarian_cancel_reservation, name='librarian_cancel_reservation'),
    
    path('librarian_approve_reservation/<int:reservation_id>/', views.librarian_approve_reservation, name='librarian_approve_reservation'),

    path('librarianaddbook/', views.librarian_add_book, name='librarian_add_book'),  
    
    path('librarianoverduebooks/', views.librarian_overdue, name='librarian_overdue_books'),  
    
    path('librarianreturnbook/<int:book_id>/<int:member_id>/', views.librarian_mark_returned, name='librarian_mark_returned'),  
    
    path('librarianfinelist', views.librarian_fine_list, name='librarian_finelist'),  
    
    path('librarianissuedbooks', views.librarian_issued_book, name='librarian_issued_books'),
    
    path('librarianreturnedbooks', views.librarian_returned_booksView, name='librarian_returned_booksview'),
    
    path('librarianpurchasedbooks', views.librarian_purchased_books, name='librarian_purchased_books'),
    
    path('librarianborrowinglist', views.librarian_borrowing_list, name='librarian_borrowing_list'),
     
    
    
    
    
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)