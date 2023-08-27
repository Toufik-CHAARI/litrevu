from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.conf import settings
from django.conf.urls.static import static
from . import forms
from . import models


@login_required
def home(request):
    return render (request,'articles/index.html')

@login_required
def add_article(request):
    article_form = forms.TicketForm()
    if request.method == 'POST':
        article_form = forms.TicketForm(request.POST, request.FILES)  # Include FILES for image handling

        if article_form.is_valid():
            ticket = article_form.save(commit=False)  
            ticket.user = request.user  
            ticket.save()
            return redirect('ticket-list')
    context = {
        'article_form': article_form,
    }
    return render(request, 'articles/create_blog_post.html', context=context)

@login_required
def ticket_list(request):
    tickets = models.Ticket.objects.all()
    context = {
        'tickets': tickets
    }
    return render(request, 'articles/ticket_list.html', context)

@login_required
def update_ticket(request, ticket_id):
    ticket_instance = get_object_or_404(models.Ticket, id=ticket_id)
    
    if request.method == 'POST':
        article_form = forms.TicketForm(request.POST, instance=ticket_instance)
        photo_form = forms.ImageForm(request.POST, request.FILES, instance=ticket_instance)
        
        if all([article_form.is_valid(), photo_form.is_valid()]):
            article_form.save()
            photo_form.save()
            return redirect('ticket-list')
    
    else:
        article_form = forms.TicketForm(instance=ticket_instance)
        photo_form = forms.ImageForm(instance=ticket_instance)
    
    context = {
        'article_form': article_form,
        'photo_form': photo_form,
    }
    
    return render(request, 'articles/update_ticket.html', context)

@login_required
def create_ticket_and_review(request):
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():            
            ticket = ticket_form.save(commit=False)  
            ticket.user = request.user  
            ticket.save()            
            
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user  
            review.save()

            return redirect('ticket-list') 

    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    return render(request, 'articles/create_ticket_and_review.html', {
        'ticket_form': ticket_form,
        'review_form': review_form,
    })

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    
    try:
        review = models.Review.objects.get(ticket=ticket)
    except models.Review.DoesNotExist:
        review = None

    context = {
        'ticket': ticket,
        'review': review
    }

    return render(request, 'articles/ticket_detail.html', context)