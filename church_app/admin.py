from django.contrib import admin
from .models import (
    Event, Sermon, BlogPost, PrayerRequest, 
    ContactMessage, Donation, Ministry
)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location')
    list_filter = ('start_date',)
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_date'

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date', 'scripture_reference')
    list_filter = ('date', 'preacher')
    search_fields = ('title', 'description', 'scripture_reference')
    date_hierarchy = 'date'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_private', 'submitted_date')
    list_filter = ('status', 'is_private', 'submitted_date')
    search_fields = ('name', 'email', 'request')
    date_hierarchy = 'submitted_date'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'submitted_date', 'is_read')
    list_filter = ('is_read', 'submitted_date')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'submitted_date'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = ['mark_as_read']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'donation_type', 'is_recurring', 'donation_date')
    list_filter = ('donation_type', 'is_recurring', 'donation_date')
    search_fields = ('name', 'email', 'transaction_id', 'notes')
    date_hierarchy = 'donation_date'

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'meeting_time')
    search_fields = ('name', 'description', 'leader')

# Customize admin site
admin.site.site_header = "Church Admin Dashboard"
admin.site.site_title = "Church Admin Portal"
admin.site.index_title = "Welcome to Church Admin Portal"