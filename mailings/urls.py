from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import MessageListView, MessageDetailView, MessageCreateView, MessageDeleteView, MessageUpdateView, \
    ClientListView, ClientDetailView, ClientCreateView, ClientDeleteView, ClientUpdateView, MailingListView, \
    MailingDetailView, MailingCreateView, MailingDeleteView, MailingUpdateView, HomeView

app_name = MailingsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('mailings/message_list', MessageListView.as_view(), name='message_list'),
    path('mailings/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
    path('mailings/create', MessageCreateView.as_view(), name='message_create'),
    path('mailings/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
    path('mailings/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
    path('mailings/client', ClientListView.as_view(), name='client_list'),
    path('mailings/client/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('mailings/client/create', ClientCreateView.as_view(), name='client_create'),
    path('mailings/client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),
    path('mailings/client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('mailings/mailing', MailingListView.as_view(), name='mailing_list'),
    path('mailings/mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/mailing/create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/mailing/<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/mailing/<int:pk>/update', MailingUpdateView.as_view(), name='mailing_update'),
]
