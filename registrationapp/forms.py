from django import forms
from django.forms import ValidationError, formset_factory
from events.models import SubEvent
from .models import Participant


class RegistrationForm(forms.ModelForm):
    sub_event = forms.ModelChoiceField(
        queryset=SubEvent.objects.all(),  # Load all sub-events
        widget=forms.HiddenInput(),  # Hide the field (auto-filled)
    )
    
    class Meta:
        model = Participant
        fields = ['full_name', 'email', 'college_name', 'dept', 'year_of_study', 'contact_number', 'emergency_contact', 'sub_event']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        sub_event = cleaned_data.get('sub_event')

        if Participant.objects.filter(email=email, sub_event=sub_event).exists():
            raise ValidationError("You have already registered for this event.")

        return cleaned_data


class TeamRegistrationForm(forms.Form):
    # choices = ['Cricket', 'Football', 'Voleyball', 'Kabaddi']
    # fields = ['fullname','college', 'year_of_study', 'email', 'contact_number', 'emergency_contact']
    teamname = forms.CharField(label="Team Name", max_length=50)
    playername = forms.CharField(label="Playe Name", max_length=50)
    year_of_study = forms.CharField(label="Year of Study", max_length=10)
    contact_number = forms.CharField(label="Contact Number", max_length=10)
    # sport = forms.ChoiceField(label="Sport", choices=choices)

PlayerFormSet = formset_factory(TeamRegistrationForm, extra=3)