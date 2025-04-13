from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from .models import (
    Event, Sermon, BlogPost, PrayerRequest, 
    ContactMessage, Donation, Ministry
)
from .forms import ContactForm, PrayerRequestForm, DonationForm

# Home View
def home(request):
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:3]
    latest_sermons = Sermon.objects.all().order_by('-date')[:3]
    latest_posts = BlogPost.objects.all().order_by('-published_date')[:3]
    
    context = {
        'upcoming_events': upcoming_events,
        'latest_sermons': latest_sermons,
        'latest_posts': latest_posts,
    }
    return render(request, 'church_app/index.html', context)

# Contact Views
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification to admin
            subject = f"New Contact Message: {contact_message.subject}"
            message = f"You have received a new contact message from {contact_message.name} ({contact_message.email}):\n\n{contact_message.message}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
            
            messages.success(request, "Your message has been sent successfully. We'll get back to you soon!")
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'church_app/contact.html', {'form': form})

# Event Views
class EventListView(ListView):
    model = Event
    template_name = 'church_app/events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(start_date__gte=timezone.now()).order_by('start_date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'church_app/events/event_detail.html'
    context_object_name = 'event'

# Sermon Views
class SermonListView(ListView):
    model = Sermon
    template_name = 'church_app/sermons/sermon_list.html'
    context_object_name = 'sermons'
    paginate_by = 10
    ordering = ['-date']

class SermonDetailView(DetailView):
    model = Sermon
    template_name = 'church_app/sermons/sermon_detail.html'
    context_object_name = 'sermon'

# Blog Views
class BlogListView(ListView):
    model = BlogPost
    template_name = 'church_app/blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ['-published_date']

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'church_app/blog/blog_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

# Ministry Views
class MinistryListView(ListView):
    model = Ministry
    template_name = 'church_app/ministries/ministry_list.html'
    context_object_name = 'ministries'

class MinistryDetailView(DetailView):
    model = Ministry
    template_name = 'church_app/ministries/ministry_detail.html'
    context_object_name = 'ministry'

# Prayer Request Views
class PrayerRequestCreateView(CreateView):
    model = PrayerRequest
    form_class = PrayerRequestForm
    template_name = 'church_app/prayer/prayer_request_form.html'
    success_url = reverse_lazy('prayer_request_thanks')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your prayer request has been submitted.")
        
        # Send email notification to admin
        subject = "New Prayer Request Submitted"
        message = f"A new prayer request has been submitted by {form.instance.name}."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
        
        return response

def prayer_request_thanks(request):
    return render(request, 'church_app/prayer/prayer_request_thanks.html')

class PrayerRequestListView(ListView):
    model = PrayerRequest
    template_name = 'church_app/prayer/prayer_request_list.html'
    context_object_name = 'prayer_requests'
    paginate_by = 10
    
    def get_queryset(self):
        # Only show non-private prayer requests
        return PrayerRequest.objects.filter(is_private=False).order_by('-submitted_date')

# Donation Views
class DonationCreateView(CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'church_app/donation/donation_form.html'
    success_url = reverse_lazy('donation_thanks')
    
    def form_valid(self, form):
        # In a real implementation, you would process the payment here
        # For this example, we'll just save the donation record
        response = super().form_valid(form)
        messages.success(self.request, "Thank you for your donation!")
        
        # Send email notification to admin and donor
        subject = "Thank You for Your Donation"
        message = f"Dear {form.instance.name},\n\nThank you for your donation of ${form.instance.amount} to our church. Your generosity helps us continue our mission.\n\nBlessings,\nChurch Staff"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [form.instance.email])
        
        admin_subject = f"New Donation: ${form.instance.amount}"
        admin_message = f"A new donation has been made by {form.instance.name} ({form.instance.email}) for ${form.instance.amount} to the {form.instance.get_donation_type_display()} fund."
        send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
        
        return response

def donation_thanks(request):
    return render(request, 'church_app/donation/donation_thanks.html')

# Resources View
def resources(request):
    sermons = Sermon.objects.all().order_by('-date')[:5]
    context = {
        'sermons': sermons,
    }
    return render(request, 'church_app/resources.html', context)

# Search View
def search_view(request):
    query = request.GET.get('q', '')
    
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
        
        sermons = Sermon.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(preacher__icontains=query) |
            Q(scripture_reference__icontains=query)
        )
        
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )
        
        ministries = Ministry.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(leader__icontains=query)
        )
    else:
        events = Event.objects.none()
        sermons = Sermon.objects.none()
        posts = BlogPost.objects.none()
        ministries = Ministry.objects.none()
    
    context = {
        'query': query,
        'events': events,
        'sermons': sermons,
        'posts': posts,
        'ministries': ministries,
    }
    
    return render(request, 'church_app/search_results.html', context)