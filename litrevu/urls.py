"""litrevu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

import authentication.views
import articles.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', articles.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('article/create/', articles.views.add_post, name='add_article'),
    path('tickets/', articles.views.post_list, name='ticket-list'),
    path('update_ticket/<int:ticket_id>/', articles.views.update_post, name='update_ticket'),
    path('article/create_ticket_and_review/', articles.views.create_post_and_review, name='add_ticket_and_review'),
    path('ticket_detail/<int:ticket_id>/', articles.views.post_detail, name='ticket_detail'),
    path('delete_ticket/<int:ticket_id>/', articles.views.delete_post, name='delete_ticket'),
    path('update_review/<int:review_id>/', articles.views.update_review, name='update_review'),
    path('add_review_to_ticket/<int:ticket_id>/', articles.views.add_review_to_ticket, name='add_review_to_ticket'),
    path('delete_review/<int:review_id>/', articles.views.delete_review, name='delete_review'),
    path('follow/<int:user_id>/', articles.views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', articles.views.unfollow_user, name='unfollow_user'),
    path('Abonnements', articles.views.user_search, name='user_search'),
    path('flux', articles.views.user_feed, name='user_feed'),


    
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)