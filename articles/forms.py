
from . import models 
from django import forms


class TicketForm(forms.ModelForm) :
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        #fields = '__all__'
        


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['image']
        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        #fields = ['ticket', 'rating', 'headline', 'body', 'user']
        fields = ['rating', 'headline', 'body']