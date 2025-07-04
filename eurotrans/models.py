from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=5000)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # ✅ Champ pour savoir si le message est lu
    date_sent = models.DateTimeField(auto_now_add=True)  # ✅ Champ pour la date et l'heure d'envoi du message

    def __str__(self):
        return f"{self.email} - {self.subject}"
    

from django.db import models
from django.core.validators import validate_email

class Subscriber(models.Model):
    email = models.EmailField(unique=True, validators=[validate_email])
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
##################################################################################

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Newsletter(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.subject

class NewsletterAttachment(models.Model):
    newsletter = models.ForeignKey(Newsletter, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='newsletter_attachments/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pièce jointe pour {self.newsletter.subject}"