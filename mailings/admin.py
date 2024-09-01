from django.contrib import admin

from mailings.models import Message, Client, Mailing, MailAttempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'head', 'body',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'first_mailing_date', 'next_mailing_date', 'period', 'status')


@admin.register(MailAttempt)
class MailAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt_time', 'status', 'server_answer', 'mail')
