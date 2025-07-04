from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    # Pages principales
    path('', views.index, name='home'),
    path('a-propos/', views.AboutView.as_view(), name='about'),
    path('notre-histoire/', views.HistoryView.as_view(), name='history'),
    path('valeurs-engagements/', views.ValuesView.as_view(), name='values'),
    path('nos-projets/', views.ProjectsView.as_view(), name='projects'),
    path('carrieres/', views.CareersView.as_view(), name='careers'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # URLs pour les branches
    path('branches/import-export/', views.ImportExportView.as_view(), name='import_export'),
    path('branches/produits-petroliers/', views.PetroleumView.as_view(), name='petroleum'),
    path('branches/construction-logements/', views.HousingView.as_view(), name='housing'),
    path('branches/education/', views.EducationView.as_view(), name='education'),
    path('branches/sante/', views.HealthcareView.as_view(), name='healthcare'),
    path('branches/infrastructures/', views.InfrastructureView.as_view(), name='infrastructure'),
    path('branches/banque/', views.BankingView.as_view(), name='banking'),
    path('branches/finance/', views.BankingView.as_view(), name='banking'),
    path('branches/entrepreneuriat/', views.EntrepreneurshipView.as_view(), name='entrepreneurship'),
    path('branches/developpement/', views.DevelopmentView.as_view(), name='development'),
    
    # Actualités
    path('contact/', views.contact, name='contact'),
    path('login/<int:pk>/', views.login, name='login'),



    path('messages/', views.list_messages, name='list_messages'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribers/', views.SubscriberListView.as_view(), name='subscribers'),

    path('newsletters/', views.NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/new/', views.NewsletterCreateView.as_view(), name='newsletter_create'),


    path('<int:pk>/preview/', views.NewsletterPreviewView.as_view(), name='preview'),
    path('<int:pk>/send/', views.NewsletterSendView.as_view(), name='newsletter_send'),
    path('<int:pk>/attachments/', views.NewsletterAttachmentListView.as_view(), name='newsletter_attachments'),  # à créer
    path('newsletter/<int:pk>/delete/', views.newsletter_delete, name='newsletter_delete'),
]
