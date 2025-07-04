# views.py
from django.shortcuts import render, get_object_or_404

# Page d'accueil
def index(request):
    return render(request, 'index.html')

from django.shortcuts import render
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'about.html'

class HistoryView(TemplateView):
    template_name = 'history.html'

class ValuesView(TemplateView):
    template_name = 'values.html'

class ProjectsView(TemplateView):
    template_name = 'projects.html'

class CareersView(TemplateView):
    template_name = 'careers.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

# Views pour les différentes branches
class ImportExportView(TemplateView):
    template_name = 'branches/import_export.html'

class PetroleumView(TemplateView):
    template_name = 'branches/petroleum.html'

class HousingView(TemplateView):
    template_name = 'branches/housing.html'

class EducationView(TemplateView):
    template_name = 'branches/education.html'

class HealthcareView(TemplateView):
    template_name = 'branches/healthcare.html'

class InfrastructureView(TemplateView):
    template_name = 'branches/infrastructure.html'

class BankingView(TemplateView):
    template_name = 'branches/banking.html'

class EntrepreneurshipView(TemplateView):
    template_name = 'branches/entrepreneurship.html'

class DevelopmentView(TemplateView):
    template_name = 'branches/development.html'

from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import Newsletter, Subscriber, NewsletterAttachment
from .forms import NewsletterForm


# Page de contact


def login(request, pk):

    return render(request, 'login.html', {

    })

# Page de contact
from .forms import ContactForm
# Vue pour gérer le formulaire de contact
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('contact')  # Redirige vers la même page pour vider le formulaire
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier vos informations.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

######################################################################################
######################################################################################
# Vue pour afficher les messages enregistrés
def list_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'message/list_messages.html', {'messages_list': messages_list})
######################################################################################
######################################################################################
# Vue pour afficher un message en détail
def message_detail(request, message_id):
    message = ContactMessage.objects.get(id=message_id)
        # ✅ Marquer comme lu si ce n'est pas déjà fait
    if not message.is_read:
        message.is_read = True
        message.save()

    return render(request, 'message/message_detail.html', {'message': message})
######################################################################################
######################################################################################
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ContactMessage

def delete_message(request, message_id):
    """ Vue pour supprimer un message via AJAX """
    if request.method == "POST":
        message = get_object_or_404(ContactMessage, id=message_id)
        message.delete()
        return JsonResponse({"success": True})  # Retourne une réponse JSON
    return JsonResponse({"success": False, "error": "Requête invalide"})


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubscriptionForm
from django.conf import settings

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            # Envoyer l'email de confirmation
            subject = 'Confirmation d\'abonnement'
            message = f'''Merci de vous être abonné à notre bulletin!
            
Vous recevrez régulièrement nos dernières actualités, offres spéciales et conseils.

Cordialement,
L'équipe de {settings.SITE_NAME}'''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Merci pour votre abonnement! Un email de confirmation vous a été envoyé.')
            return redirect('home')
    else:
        form = SubscriptionForm()
    
    return render(request, 'abonnement/subscribe.html', {'form': form})

##################################################################################################################

class SubscriberListView(ListView):
    model = Subscriber
    template_name = 'abonnement/subscribers.html'
    context_object_name = 'subscribers'
    paginate_by = 20


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'abonnement/newslist.html'
    context_object_name = 'newsletters'
    ordering = ['-created_at']
    paginate_by = 10

class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'abonnement/compose.html'
    success_url = reverse_lazy('newsletter_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Gestion simplifiée des pièces jointes
        for file in self.request.FILES.getlist('attachments'):
            NewsletterAttachment.objects.create(newsletter=self.object, file=file)
        
        if form.cleaned_data['is_published']:
            self.send_newsletter()
        
        return response

    def send_newsletter(self):
        subscribers = Subscriber.objects.filter(is_active=True).values_list('email', flat=True)
        if not subscribers:
            messages.warning(self.request, "Aucun abonné actif.")
            return
        
        email = EmailMessage(
            self.object.subject,
            self.object.content,
            settings.DEFAULT_FROM_EMAIL,
            bcc=list(subscribers))
        
        for attachment in self.object.attachments.all():
            email.attach(attachment.file.name, attachment.file.read())
        
        email.send()
        self.object.sent_at = timezone.now()
        self.object.save()
        messages.success(self.request, f"Newsletter envoyée à {len(subscribers)} abonnés.")


class NewsletterPreviewView(DetailView):
    model = Newsletter
    template_name = 'abonnement/preview.html'


class NewsletterAttachmentListView(DetailView):
    model = Newsletter
    template_name = 'abonnement/newsletter_attachments.html'
    context_object_name = 'newsletter'


class NewsletterSendView(DetailView):
    model = Newsletter
    template_name = 'abonnement/newsletter_confirm_send.html'

    def post(self, request, *args, **kwargs):
        newsletter = self.get_object()
        if newsletter.sent_at:
            messages.warning(request, "Cette newsletter a déjà été envoyée.")
            return redirect('newsletter_list')
        
        subscribers = Subscriber.objects.filter(is_active=True)
        if not subscribers:
            messages.warning(request, "Aucun abonné actif.")
            return redirect('newsletter_list')
        
        try:
            email = EmailMessage(
                newsletter.subject,
                newsletter.content,
                settings.DEFAULT_FROM_EMAIL,
                bcc=[s.email for s in subscribers]
            )
            for attachment in newsletter.attachments.all():
                email.attach(attachment.file.name, attachment.file.read())
            
            email.send()
            newsletter.sent_at = timezone.now()
            newsletter.save()
            messages.success(request, f"Envoyée à {len(subscribers)} abonnés.")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
        
        return redirect('newsletter_list')


def newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    
    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, "La newsletter a été supprimée avec succès.")
        return redirect('newsletter_list')  # Remplace par ton URL de retour après suppression

    return render(request, 'abonnement/newsletter_confirm_delete.html', {'newsletter': newsletter})