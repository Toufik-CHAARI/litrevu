from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.conf import settings
from django.conf.urls.static import static
from . import forms
from . import models
from django.contrib import messages
from django.contrib.auth import get_user_model
from authentication.models import User
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Value, CharField
from .models import Ticket, Review, UserFollows



@login_required
def home(request):
    return render (request,'articles/index.html')

@login_required
def add_article(request):
    article_form = forms.TicketForm()
    if request.method == 'POST':
        article_form = forms.TicketForm(request.POST, request.FILES)  

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
    
    if ticket_instance.user != request.user:
        # Return the user to a suitable page with a warning message or use the modal approach
        # I'll use the modal approach here:
        context = {
            'not_owner': True,
        }
        return render(request, 'articles/update_ticket.html', context)

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket_instance)
        #article_form = forms.TicketForm(request.POST, instance=ticket_instance)
        #photo_form = forms.ImageForm(request.POST, request.FILES, instance=ticket_instance)
        
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect('ticket-list')
    else:
        ticket_form = forms.TicketForm(instance=ticket_instance)
    
    context = {
        'ticket_form': ticket_form,
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
        reviews = models.Review.objects.filter(ticket=ticket)
    except models.Review.DoesNotExist:
        review = None
    user_has_reviewed = models.Review.objects.filter(ticket=ticket, user=request.user).exists()
    context = {
        'ticket': ticket,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
    }

    return render(request, 'articles/ticket_detail.html', context)

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    
    if request.method == 'POST':
        if request.user == ticket.user:
            ticket.delete()
            return redirect('ticket-list')
        else:
            return redirect('ticket-detail', ticket_id=ticket_id)
    
    context = {
        'ticket': ticket,
        'not_owner': request.user != ticket.user
    }
    return render(request, 'articles/delete_ticket.html', context)

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
        return redirect('ticket-list')  

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
    not_owner = request.user != review.user and not request.user.has_perm('articles.delete_review')
   
    if request.method == 'POST' and not not_owner:
        review.delete()
        return redirect('ticket-list')
    
    context = {
        'review': review,
        'not_owner': not_owner
    }
    return render(request, 'articles/confirm_delete_review.html', context)

    

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        models.UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.username}!")
    else:
        messages.error(request, "You can't follow yourself!")
    return redirect('user_search')  

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    try:
        follow_relation = models.UserFollows.objects.get(user=request.user, followed_user=user_to_unfollow)
        follow_relation.delete()
        messages.success(request, f"You have unfollowed {user_to_unfollow.username}.")
    except models.UserFollows.DoesNotExist:
        messages.error(request, "You weren't following this user.")
    return redirect('user_search')  


@login_required
def user_search(request):
    query = request.GET.get('q')
    users = []
    if query:
        users = get_user_model().objects.filter(username__icontains=query).exclude(id=request.user.id)
        
    results = []
    for user in users:
        followed = request.user.following.filter(followed_user=user).exists()
        results.append({'user': user, 'followed': followed})

    followers = request.user.followed_by.all()
    following = request.user.following.all()
    user_not_found = False
    if query and not users:
        user_not_found = True

    context = {
        'results': results,
        'followers': followers,
        'following': following,
        'user_not_found': user_not_found
    }

    return render(request, 'articles/user_search.html', context)






@login_required
def user_feed(request):
    from django.db.models import Value, CharField      
    followed_users = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    
    from django.db.models import F
        
    following_reviews = Review.objects.filter(user__in=followed_users).values(
        'id', 'headline', 'body', 'rating', 'time_created', 'ticket_id', 'user__username', 'ticket__title', 'ticket__user__username'
    ).annotate(
        content_type=Value('review', CharField()),
        ticket_title=F('ticket__title'),
        ticket_author=F('ticket__user__username')
    )    
    
    
    following_tickets = Ticket.objects.filter(user__in=followed_users).values('id', 'title', 'description', 'image', 'time_created', 'user__username').annotate(content_type=Value('ticket', CharField())).order_by('-time_created')
    my_tickets = Ticket.objects.filter(user=request.user).values('id', 'title', 'description', 'image', 'time_created', 'user__username').annotate(content_type=Value('ticket', CharField())).order_by('-time_created')
    my_reviews = Review.objects.filter(user=request.user).values(
    'id', 'headline', 'body', 'rating', 'time_created', 
    'ticket_id', 'user__username', 'ticket__title'
    ).annotate(content_type=Value('review', CharField())).order_by('-time_created')
    
    my_ticket_reviews = Review.objects.filter(ticket__user=request.user).values(
    'id', 'headline', 'body', 'rating', 'time_created', 'ticket_id', 
    'ticket__title', 'user__username', 'ticket__image'  # Add 'ticket__image' here
    ).annotate(content_type=Value('review', CharField())).order_by('-time_created')

    
    
    context = {
        'following_tickets': following_tickets,
        'my_tickets': my_tickets,
        'my_reviews': my_reviews,
        'my_ticket_reviews': my_ticket_reviews,
        'following_reviews': following_reviews
    }

   
    if following_tickets:
        print(following_tickets[0]['user__username'])
    

    return render(request, 'articles/user_feed.html', context)

