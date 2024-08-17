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
    
    path('', views.member_reg),
    
    path('memberregistration/', views.member_reg),
    
    path('login/', views.logins),
    
    path('homepage/', views.admin_home),
    
    path('logouts/',views.logouts),
    
    path('studentlist/',views.view_studentlist),
    
    path('studentrequest/', views.student_request),
    
    path('adminapprovestudent/<int:id>',views.admin_approve_student),
    
    path('admindeletestudent/<int:id>',views.admin_delete_student),
    
    path('admindeletemember/<int:id>',views.admin_delete_member),
    
    # path('adminviewmember/<int:id>', views.admin_view_member),
    
    path('adminaddmembers/', views.admin_add_members),
    
    path('adminactivatemember/<int:id>',views.admin_activate_member),
    
    path('admindeactivatemember/<int:id>',views.admin_deactivate_member),
    
    path('addbook', views.add_book),  
    
    path('adminaddlibrarian', views.admin_add_librarian),
    
    path('memberhomepage/', views.member_homepage),
    
    path('librarianhomepage/', views.librarian_homepage),
    
    path('searchresult/', views.search_book),
    
    path('viewbook/<int:id>', views.view_book),
    
    

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)