"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from frazzetoBookReview.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/books/', BookView.as_view(), name='book'),
    path('api/review/', ReviewView.as_view(), name='review'),
    path('api/courses/<int:id>/', CourseView.as_view({"patch": "partial_update","delete": "destroy"}), name='course'),
    path('api/courses/', CourseView.as_view({"get": "retrieve","post": "create"}), name='course'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/courses/join/', JoinCourseView.as_view(), name='join-course'),
    path('api/assignments/', AssignmentReviewView.as_view(), name='assignment-list-create'),
    path('api/review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='assignment-delete'),
    path('api/books/update/<int:pk>/', BookDetailView.as_view(), name='book-update-delete'),
    path('api/users/<int:id>/', IdToUser.as_view(), name='user-detail'),

]
