from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Events
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    
    # Sermons
    path('sermons/', views.SermonListView.as_view(), name='sermon_list'),
    path('sermons/<int:pk>/', views.SermonDetailView.as_view(), name='sermon_detail'),
    
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    
    # Ministries
    path('ministries/', views.MinistryListView.as_view(), name='ministry_list'),
    path('ministries/<int:pk>/', views.MinistryDetailView.as_view(), name='ministry_detail'),
    
    # Prayer Requests
    path('prayer-requests/', views.PrayerRequestListView.as_view(), name='prayer_request_list'),
    path('prayer-requests/new/', views.PrayerRequestCreateView.as_view(), name='prayer_request_create'),
    path('prayer-requests/thanks/', views.prayer_request_thanks, name='prayer_request_thanks'),
    
    # Donations
    path('donate/', views.DonationCreateView.as_view(), name='donation_create'),
    path('donate/thanks/', views.donation_thanks, name='donation_thanks'),
    
    # Resources
    path('resources/', views.resources, name='resources'),
    
    # Search
    path('search/', views.search_view, name='search'),
]
