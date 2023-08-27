from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.conf import settings
from django.conf.urls.static import static
from . import forms
from . import models
from django.contrib import messages



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


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)    
    if request.user == ticket.user:
        ticket.delete()
        messages.success(request, 'Votre billet a été supprimé avec succès.')
    else:
        messages.error(request, 'Vous n avez pas la permission de supprimer ce billet .')

    return redirect('ticket-list')

@login_required
def update_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    
    if review.user != request.user:
        messages.error(request, "You do not have permission to edit this review.")
        return redirect('ticket-list') 

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review_form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('ticket-list')  

    else:
        review_form = forms.ReviewForm(instance=review)

    return render(request, 'articles/update_review.html', {
        'review_form': review_form,
    })
    

@login_required
def add_review_to_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    
    if models.Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(request, "You've already reviewed this ticket.")
        return redirect('ticket-list')  # or redirect to the ticket's detail page

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('ticket-list')  

    else:
        review_form = forms.ReviewForm()

    return render(request, 'articles/add_review.html', {
        'review_form': review_form,
        'ticket': ticket,
    })
    
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
   
    if request.user == review.user or request.user.has_perm('articles.delete_review'):
        if request.method == 'POST':
            review.delete()
            messages.success(request, 'Review deleted successfully!')
            return redirect('ticket-list')  
        return render(request, 'articles/confirm_delete_review.html', {'review': review})
    else:
        messages.error(request, "You don't have permission to delete this review.")
        return redirect('ticket-list')  