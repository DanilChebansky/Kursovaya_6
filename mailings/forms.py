from django.forms import BooleanField, ModelForm, DateTimeField

from mailings.models import Message, Client, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field, DateTimeField):
                field.widget.attrs['class'] = 'form-control-date'
            else:
                field.widget.attrs['class'] = 'form-control'


class MessageForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Client
        fields = '__all__'


class MailingForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Mailing
        exclude = ('is_active',)


class MailingModeratorForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Mailing
        fields = ('is_active',)
