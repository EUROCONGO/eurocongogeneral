from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, Subscriber, Newsletter, NewsletterAttachment

# Formulaire de contact
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Votre nom'),
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Votre email'),
                'id': 'email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Objet'),
                'id': 'subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Laissez un message ici'),
                'id': 'message',
                'style': 'height: 150px;'
            }),
        }


# Formulaire d'abonnement à la newsletter
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Entrez votre email')
            })
        }


# Formulaire de création de newsletter
class NewsletterForm(forms.ModelForm):
    attachments = forms.FileField(
        required=False,
        label=_('Pièces jointes'),
        help_text=_("Formats acceptés : PDF, Word, Excel, Images"),
        widget=forms.ClearableFileInput()
)


    class Meta:
        model = Newsletter
        fields = ['subject', 'content', 'is_published']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Objet')
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': _('Contenu de la newsletter')
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# Formulaire de connexion
class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Nom d'utilisateur ou email"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Votre nom d'utilisateur ou email")
        })
    )
    
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Votre mot de passe")
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        label=_("Se souvenir de moi"),
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
