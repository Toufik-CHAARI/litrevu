
from . import models 
from django import forms


class TicketForm(forms.ModelForm) :
    title = forms.CharField(label="Titre du Post", max_length=128)
    description = forms.CharField(label="Description", max_length=8192, widget=forms.Textarea)
    class Meta:
        model = models.Ticket
        fields = ['title', 'description','image']
             


RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICES, label="Votre notation")
    headline = forms.CharField(label="Titre de la critique", max_length=128)
    body = forms.CharField(label="Votre avis", max_length=8192, widget=forms.Textarea) # J'ai ajouté `widget=forms.Textarea` pour rendre le champ `body` sous forme de textarea.
    
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']