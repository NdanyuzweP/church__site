from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    description = RichTextUploadingField()
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    slides = models.FileField(upload_to='sermons/slides/', blank=True, null=True)
    scripture_reference = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.preacher}"
    
    def get_absolute_url(self):
        return reverse('sermon_detail', args=[str(self.id)])

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.slug)])

class PrayerRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('praying', 'Praying'),
        ('answered', 'Answered'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    request = models.TextField()
    is_private = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_date']
    
    def __str__(self):
        return f"Prayer request from {self.name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_date']
    
    def __str__(self):
        return f"Message from {self.name}: {self.subject}"

class Donation(models.Model):
    DONATION_TYPES = (
        ('general', 'General'),
        ('missions', 'Missions'),
        ('building', 'Building Fund'),
        ('youth', 'Youth Ministry'),
        ('children', 'Children Ministry'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES, default='general')
    is_recurring = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True)
    donation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-donation_date']
    
    def __str__(self):
        return f"{self.name} - ${self.amount} ({self.get_donation_type_display()})"

class Ministry(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField()
    leader = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    meeting_time = models.CharField(max_length=255, blank=True)
    meeting_location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='ministries/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Ministries"
        ordering = ['name']
    
    def __str__(self):
        return self.name
