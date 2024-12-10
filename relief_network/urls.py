"""
URL configuration for relief_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView # used for logout
# to direct javascript to the correct url
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView # used for logout

#from accounts.views import CustomLogoutView as CustomLogoutView__  # Adjust the import according to your file structure
from accounts import views as accounts_views
from analytics import views as analytics_views
from communication import views as communication_views
from feedback import views as feedback_views
from matching import views as matching_views
from offers import views as offers_views
from requests_app import views as requests_views
from main import views as main_views


urlpatterns = [
    # main views
    #path("",main_views.base, name='base'),# took this away as we was want the home page to be the main page
    path("", main_views.home, name='home'),
    path('about_us/', main_views.about_us, name='about_us'),
    path('faq/', main_views.faq, name='faq'),
    path('contact/', main_views.contact, name='contact'),

    # accounts views
    path('logout/', accounts_views.user_logout, name='logout'),
    path('signup/', accounts_views.signup, name='signup'),
    path('profile/edit/', accounts_views.profile_edit, name='profile_edit'),
    path('profile/', accounts_views.profile_view, name='profile_view'),
    path('login/', accounts_views.user_login, name='login'),
    

    #Reset password
    path('reset_password/', accounts_views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', PasswordResetDoneView.as_view(template_name='reset_password_done.html'), name='reset_password_done'),
    path('reset/<uidb64>/<token>/', accounts_views.CustomPasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='reset_password_complete'),
    #path('password_reset_email/', accounts_views.password_reset_email, name='password_reset_email'),
   
    # analytics views
    path('dashboard/', analytics_views.dashboard, name='dashboard'),

    # communication views
    path('inbox/', communication_views.inbox, name='inbox'),
    path('send/', communication_views.send_message, name='send_message'),
    path('view_message/<int:message_id>/', communication_views.view_message, name='view_message'),
    path('send/<int:recipient_id>/', communication_views.send_message, name='send_message_to'),
    path('delete_message/<message_id>/', communication_views.delete_message, name='delete_message'),
    
    
    
    # feedback views
    path('give_feedback/', feedback_views.give_feedback, name='give_feedback'),
    path('list_feedback/', feedback_views.feedback_list, name='feedback_list'),

    # matching views
    path('matches/', matching_views.view_matches, name='view_matches'),

    # offers views (for donors)
    path('create_offer/', offers_views.create_offer, name='create_offer'),# changed
    path('user_offer_list/', offers_views.user_offer_list, name='user_offer_list'),# look at their own offers
    path('edit_offer/<int:pk>/', offers_views.edit_offer, name='edit_offer'), # changed
    path('delete_offer/<int:pk>/', offers_views.delete_offer, name='delete_offer'), # changed
    path('user_offer_details/<int:pk>/', offers_views.user_offer_details, name='user_offer_details'),
    #path('view_requests_and_accept/', offers_views.offer_view_requests, {'page_type': 'all'}, name='view_requests_and_accept'),
    #path('view_accepted_requests/', offers_views.offer_view_requests, {'page_type': 'accepted'}, name='view_accepted_requests'),
    path('view_requests_and_accept/', offers_views.view_requests_and_accept, name='view_requests_and_accept'),
    path('view_accepted_requests/', offers_views.view_accepted_requests, name='view_accepted_requests'),
    path('offers_view_requester_detail/<int:request_id>/', offers_views.offers_view_requester_detail, name='offers_view_requester_detail'),
    path('toggle_accept/', offers_views.toggle_accept, name='toggle_accept'),
    

    
    # requests views (for beneficiaries)
    path('create_request/', requests_views.create_request, name='create_request'),
    path('user_request_list/', requests_views.user_request_list, name='user_request_list'),
    path('edit_request/<int:pk>/', requests_views.edit_request, name='edit_request'),
    path('delete_request/<int:pk>/', requests_views.delete_request, name='delete_request'),
    path('user_request_details/<int:pk>/', requests_views.user_request_details, name='user_request_details'),
    
    path('requester_view_offers/', requests_views.requester_view_offers, name='requester_view_offers'),
    path('requester_view_offers_detail/<int:offer_id>/', requests_views.requester_view_offers_detail, name='requester_view_offers_detail'),
    path('requester_liked_offers/', requests_views.requester_liked_offers, name='requester_liked_offers'),
    path('toggle_like/', requests_views.toggle_like, name='toggle_like'),
    
    #path('cancel_request/<int:pk>/', requests_views.request_cancel, name='request_cancel'),# changed
    #path('search_requests/', requests_views.search_requests, name='search_requests'),

    #path('base/', TemplateView.as_view(template_name='base.html'), name='base'),# I've created this maybe wrong
    #base help support home    
]
