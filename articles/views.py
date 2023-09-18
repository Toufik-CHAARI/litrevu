from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from . import forms
from . import models
from django.contrib import messages
from django.contrib.auth import get_user_model
from authentication.models import User
from django.db.models import Value, CharField
from .models import Ticket, Review


@login_required
def home(request):
    """
    this function renders the home page if the user is authenticated.
    """
    return render(request, "articles/index.html")


@login_required
def add_post(request):
    """
    This function handles the creation of a new post (ticket) by an
    authenticated user,processes the form submission, associates
    the ticket with the current user, and redirects to the
    post list page when submission is sucessful.
    """
    article_form = forms.TicketForm()
    if request.method == "POST":
        article_form = forms.TicketForm(request.POST, request.FILES)

        if article_form.is_valid():
            ticket = article_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("ticket-list")
    context = {
        "article_form": article_form,
    }
    return render(
        request, "articles/create_blog_post.html", context=context
    )


@login_required
def post_list(request):
    """
    Displays a list of all posts (tickets) created by users.
    Only authenticated users can access this page.
    """
    tickets = models.Ticket.objects.all()
    context = {"tickets": tickets}
    return render(request, "articles/ticket_list.html", context)


@login_required
def update_post(request, ticket_id):
    """
    This function handles the update of a user's own ticket post.
    it allows an authenticated user to update their own post
    identified by 'ticket_id'.It checks if the user is the owner
    of the ticket post; if not, it displays a notification.
    If the user is the owner, it processes the form submission for
    updating the ticket post.
    """
    ticket_instance = get_object_or_404(models.Ticket, id=ticket_id)

    if ticket_instance.user != request.user:
        context = {
            "not_owner": True,
        }
        return render(request, "articles/update_ticket.html", context)

    if request.method == "POST":
        ticket_form = forms.TicketForm(
            request.POST, request.FILES, instance=ticket_instance
        )

        if ticket_form.is_valid():
            ticket_form.save()
            return redirect("ticket-list")
    else:
        ticket_form = forms.TicketForm(instance=ticket_instance)

    context = {
        "ticket_form": ticket_form,
    }

    return render(request, "articles/update_ticket.html", context)


@login_required
def create_post_and_review(request):
    """
    This function handles the creation of both, a new post(ticket)
    and a review by an authenticated user,it allows authenticated
    users to submit a new post and a corresponding review using forms.
    It processes the form submissions, associates the ticket and
    review with the current user,and redirects to the ticket list
    page upon successful submission.
    """
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

            return redirect("ticket-list")

    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    return render(
        request,
        "articles/create_ticket_and_review.html",
        {
            "ticket_form": ticket_form,
            "review_form": review_form,
        },
    )


@login_required
def post_detail(request, ticket_id):
    """
    Displays the details of a post(ticket), including associated
    reviews, to an authenticated user.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    reviews = models.Review.objects.filter(ticket=ticket)
    user_has_reviewed = models.Review.objects.filter(
        ticket=ticket, user=request.user
    ).exists()
    context = {
        "ticket": ticket,
        "reviews": reviews,
        "user_has_reviewed": user_has_reviewed,
    }

    return render(request, "articles/ticket_detail.html", context)


@login_required
def delete_post(request, ticket_id):
    """
    This function handles the deletion of a post (ticket) by an
    authenticated user.it allows an authenticated user to delete
    a ticket identified by 'ticket_id' if they are the owner.
    If the user is not the owner of the ticket, they are redirected
    to the ticket detail page.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if request.method == "POST":
        if request.user == ticket.user:
            ticket.delete()
            return redirect("ticket-list")
        else:
            return redirect("ticket-detail", ticket_id=ticket_id)

    context = {
        "ticket": ticket,
        "not_owner": request.user != ticket.user,
    }
    return render(request, "articles/delete_ticket.html", context)


@login_required
def update_review(request, review_id):
    """
    This function handles the update of a review by an authenticated
    user.it allows an authenticated user to update an existing review
    identified by 'review_id'. It checks if the user is the owner
    of the review, and if not, redirects them to the post list page.
    If the user is the owner, it processes the form submission
    for updating the review.
    """
    review = get_object_or_404(models.Review, id=review_id)
    if review.user != request.user:
        return redirect("ticket-list")
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review_form.save()
            return redirect("ticket-list")

    else:
        review_form = forms.ReviewForm(instance=review)

    return render(
        request,
        "articles/update_review.html",
        {
            "review_form": review_form,
        },
    )


@login_required
def add_review_to_ticket(request, ticket_id):
    """
    This function handles the addition of a review to an existing
    post by an authenticated user.It allows an authenticated user
    to add a review to a specific ticket identified by 'ticket_id'.
    It checks if the user has already reviewed the ticket and prevents
    duplicate reviews. If the user hasn't reviewed the ticket,
    it processes the form submission for adding the review.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if models.Review.objects.filter(
        ticket=ticket, user=request.user
    ).exists():
        
        return redirect("ticket-list")

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("ticket-list")

    else:
        review_form = forms.ReviewForm()

    return render(
        request,
        "articles/add_review.html",
        {
            "review_form": review_form,
            "ticket": ticket,
        },
    )


@login_required
def delete_review(request, review_id):
    """
    This function handles the deletion of a review by an
    authenticated user.It allows an authenticated user to
    delete a review identified by 'review_id' if they are either
    the owner of the review or have permission to delete reviews.
    """
    review = get_object_or_404(models.Review, id=review_id)
    not_owner = (
        request.user != review.user
        and not request.user.has_perm("articles.delete_review")
    )

    if request.method == "POST" and not not_owner:
        review.delete()
        return redirect("ticket-list")

    context = {"review": review, "not_owner": not_owner}
    return render(
        request, "articles/confirm_delete_review.html", context
    )


@login_required
def follow_user(request, user_id):
    """
    This function handles the action of following another user by an
    authenticated user.It allows an authenticated user to follow
    another user identified by 'user_id'.It checks if the current
    user is not the same as the user they want to follow before
    performing the action.
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        models.UserFollows.objects.get_or_create(
            user=request.user, followed_user=user_to_follow
        )
    return redirect("user_search")


@login_required
def unfollow_user(request, user_id):
    """
    This function handles the action of unfollowing another user
    by an authenticated user.It allows an authenticated user to
    unfollow another user identified by 'user_id'.It attempts
    to find and delete the follow relationship between the
    current user and the target user.
    If no such relationship exists, it takes no action.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    try:
        follow_relation = models.UserFollows.objects.get(
            user=request.user, followed_user=user_to_unfollow
        )
        follow_relation.delete()
    except models.UserFollows.DoesNotExist:
        pass
    return redirect("user_search")


@login_required
def user_search(request):
    """
    This function handles user search and displays search results to
    an authenticated user.It allows an authenticated user to search
    for other users by their usernames.It retrieves a query parameter
    'q' from the request to perform the search.Users matching the
    search criteria are displayed along with their follow status
    (followed or not).
    """
    query = request.GET.get("q")
    users = []
    if query:
        users = (
            get_user_model()
            .objects.filter(username__icontains=query)
            .exclude(id=request.user.id)
        )

    results = []
    for user in users:
        followed = request.user.following.filter(
            followed_user=user
        ).exists()
        results.append({"user": user, "followed": followed})

    followers = request.user.followed_by.all()
    following = request.user.following.all()
    user_not_found = False
    if query and not users:
        user_not_found = True

    context = {
        "results": results,
        "followers": followers,
        "following": following,
        "user_not_found": user_not_found,
    }

    return render(request, "articles/user_search.html", context)


@login_required
def user_feed(request):
    """
    This function displays a user's activity feed, including followed
    users' tickets and reviews.It retrieves and displays a user's
    activity feed, which includes:
    - Posts (tickets) and reviews of users they follow
    - Their own post (ticket) and reviews
    - Reviews on their own posts (ticket)
    """
    followed_users = models.UserFollows.objects.filter(
        user=request.user
    ).values_list("followed_user", flat=True)

    from django.db.models import F

    following_reviews = (
        Review.objects.filter(user__in=followed_users)
        .values(
            "id",
            "headline",
            "body",
            "rating",
            "time_created",
            "ticket_id",
            "user__username",
            "ticket__title",
            "ticket__user__username",
        )
        .annotate(
            content_type=Value("review", CharField()),
            ticket_title=F("ticket__title"),
            ticket_author=F("ticket__user__username"),
        )
        .order_by("-time_created")
    )

    following_tickets = (
        Ticket.objects.filter(user__in=followed_users)
        .values(
            "id",
            "title",
            "description",
            "image",
            "time_created",
            "user__username",
        )
        .annotate(content_type=Value("ticket", CharField()))
        .order_by("-time_created")
    )
    my_tickets = (
        Ticket.objects.filter(user=request.user)
        .values(
            "id",
            "title",
            "description",
            "image",
            "time_created",
            "user__username",
        )
        .annotate(content_type=Value("ticket", CharField()))
        .order_by("-time_created")
    )
    my_reviews = (
        Review.objects.filter(user=request.user)
        .values(
            "id",
            "headline",
            "body",
            "rating",
            "time_created",
            "ticket_id",
            "user__username",
            "ticket__title",
        )
        .annotate(content_type=Value("review", CharField()))
        .order_by("-time_created")
    )

    my_ticket_reviews = (
        Review.objects.filter(ticket__user=request.user)
        .values(
            "id",
            "headline",
            "body",
            "rating",
            "time_created",
            "ticket_id",
            "ticket__title",
            "user__username",
            "ticket__image",  
        )
        .annotate(content_type=Value("review", CharField()))
        .order_by("-time_created")
    )

    context = {
        "following_tickets": following_tickets,
        "my_tickets": my_tickets,
        "my_reviews": my_reviews,
        "my_ticket_reviews": my_ticket_reviews,
        "following_reviews": following_reviews,
    }

    if following_tickets:
        print(following_tickets[0]["user__username"])
    return render(request, "articles/user_feed.html", context)
