"""
URL configuration for seph_v2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from user import views as user_views
from property import views as property_views
from chat import views as chat_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='user/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='user/logout.html'),
         name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset.html'
         ),
         name='password_reset'), 
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('', property_views.home, name='Home'),
    path('about/', property_views.about, name='about'),
    path('profile/', user_views.profile, name='profile'),
    path('user/<int:pk>', user_views.UserProfile.as_view(), name='user'),
    path('property/', property_views.PropertyList.as_view(), name='property'),
    path('property/<int:pk>/', property_views.PropertyDetails.as_view(),
         name='propertydetails'),
    path('property/post/', property_views.propertyPost, name='propertypost'),
    path('property/post/<int:property_id>/', property_views.propertyPost,
         name='property_update'),
    path('property/delete/<int:property_id>/', property_views.delete_property_post, name='delete_property_post'),

    path('ajax/load-subcities/', property_views.load_subcities,
         name='ajax_load_subcities'),
    path('chat-rooms/', chat_views.user_chat_rooms,
         name='user_chat_rooms'),
    path('chat-room/<int:recipient_id>/', chat_views.chat_room_messages,
         name='chat_room_messages'),
    path('chat-room/<int:recipient_id>/<int:property_id>/',
         chat_views.chat_room_messages,
         name='chat_room_messages_with_property'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
