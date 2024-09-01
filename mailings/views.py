from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from blog.services import get_articles_from_cache
from mailings.forms import MessageForm, ClientForm, MailingForm, MailingModeratorForm
from mailings.models import Message, Client, Mailing


class HomeView(TemplateView):
    """
    Контроллер главной страницы сайта
    """
    template_name = 'mailings/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = Mailing.objects.all()
        clients = Client.objects.all()
        context_data['all_mailings'] = mailings.count()
        context_data['active_mailings'] = mailings.filter(is_active=True).count()
        context_data['active_clients'] = clients.values('email').distinct().count()

        context_data['random_blogs'] = get_articles_from_cache().order_by('?')[:3]
        return context_data


class MessageListView(ListView, LoginRequiredMixin):
    model = Message


class MessageCreateView(CreateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.user_owner = user
        product.save()
        return super().form_valid(form)


class MessageDetailView(DetailView, LoginRequiredMixin):
    model = Message


class MessageUpdateView(UpdateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(DeleteView, LoginRequiredMixin):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class ClientListView(ListView, LoginRequiredMixin):
    model = Client


class ClientCreateView(CreateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.user_owner = user
        product.save()
        return super().form_valid(form)


class ClientDetailView(DetailView, LoginRequiredMixin):
    model = Client


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class MailingListView(ListView, LoginRequiredMixin):
    model = Mailing


class MailingCreateView(CreateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.user_owner = user
        product.save()
        return super().form_valid(form)


class MailingDetailView(DetailView, LoginRequiredMixin):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['client_lst'] = []
        counter = 0
        while len(context_data['client_lst']) < len(self.object.client.all()):
            if self.object.client.filter(pk=str(counter+1)).exists():
                context_data['client_lst'].append(self.object.client.get(pk=str(counter+1)).name)
            counter += 1
        context_data['attempt_list'] = self.object.attempts.all()
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.has_perm('mailings.can_view_mailing_detail') or user == self.object.owner:
            return self.object
        raise PermissionDenied


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm('mailings.set_active'):
            return MailingModeratorForm
        raise PermissionDenied


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')
