from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import ContactForm, DonationForm, FoodRequestForm, UserRegisterForm
from .models import Donation, FoodRequest


def splash(request: HttpRequest) -> HttpResponse:
    redirect_url = reverse("home")
    return render(request, "splash.html", {"redirect_url": redirect_url})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("splash")


def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    latest_donations = Donation.objects.filter(status=Donation.Status.AVAILABLE).order_by("-available_till")[:6]
    return render(request, "home.html", {"latest_donations": latest_donations})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")


def contact(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us. We'll get back soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome aboard!")
            return redirect("dashboard")
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    donations = requests_sent = requests_received = None
    if request.user.is_donor:
        donations = Donation.objects.filter(donor=request.user).prefetch_related("requests__receiver")
        requests_received = FoodRequest.objects.filter(donation__donor=request.user).select_related(
            "donation", "receiver"
        )
    else:
        requests_sent = FoodRequest.objects.filter(receiver=request.user).select_related("donation")
    return render(
        request,
        "dashboard.html",
        {
            "donations": donations,
            "requests_received": requests_received,
            "requests_sent": requests_sent,
        },
    )


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    donations_qs = Donation.objects.filter(donor=request.user).order_by("-created_at")
    requests_sent_qs = FoodRequest.objects.filter(receiver=request.user).select_related("donation").order_by("-timestamp")
    requests_received_qs = FoodRequest.objects.filter(donation__donor=request.user).select_related(
        "donation", "receiver"
    ).order_by("-timestamp")

    if request.user.is_donor:
        stats = {
            "total_donations": donations_qs.count(),
            "claimed_donations": donations_qs.filter(status=Donation.Status.CLAIMED).count(),
            "requests_received": requests_received_qs.count(),
            "accepted_requests_received": requests_received_qs.filter(status=FoodRequest.Status.ACCEPTED).count(),
        }
    else:  # Receiver
        stats = {
            "requests_sent": requests_sent_qs.count(),
            "accepted_requests": requests_sent_qs.filter(status=FoodRequest.Status.ACCEPTED).count(),
            "pending_requests": requests_sent_qs.filter(status=FoodRequest.Status.PENDING).count(),
        }

    context = {
        "user_obj": request.user,
        "recent_donations": donations_qs[:5],
        "recent_requests_sent": requests_sent_qs[:5],
        "recent_requests_received": requests_received_qs[:5],
        "stats": stats,
    }
    return render(request, "profile.html", context)


@login_required
def donation_list(request: HttpRequest) -> HttpResponse:
    donations = (
        Donation.objects.select_related("donor")
        .filter(status=Donation.Status.AVAILABLE, available_till__gte=timezone.now())
        .order_by("available_till")
    )
    location = request.GET.get("location")
    food_type = request.GET.get("food_name")
    
    if location:
        # Normalize the search query: remove spaces and convert to lowercase
        location_query = location.lower().strip()
        # Use icontains for case-insensitive search
        donations = donations.filter(address__icontains=location_query)
        
    if food_type:
        donations = donations.filter(food_name__icontains=food_type)
    return render(request, "donations/list.html", {"donations": donations})


@login_required
def donation_create(request: HttpRequest) -> HttpResponse:
    if not request.user.is_donor:
        messages.error(request, "Only donors can create donations.")
        return redirect("donation_list")
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            messages.success(request, "Donation listed successfully.")
            return redirect("dashboard")
    else:
        form = DonationForm()
    return render(request, "donations/form.html", {"form": form})


@login_required
def donation_edit(request: HttpRequest, pk: int) -> HttpResponse:
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    if request.method == "POST":
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, "Donation updated successfully.")
            return redirect("dashboard")
    else:
        form = DonationForm(instance=donation)
    return render(request, "donations/form.html", {"form": form, "donation": donation})


@login_required
@require_POST
def donation_delete(request: HttpRequest, pk: int) -> HttpResponse:
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    donation.delete()
    messages.success(request, "Donation deleted successfully.")
    return redirect("dashboard")


@login_required
def create_food_request(request: HttpRequest, pk: int) -> HttpResponse:
    donation = get_object_or_404(Donation, pk=pk, status=Donation.Status.AVAILABLE)
    if donation.donor == request.user:
        messages.error(request, "You cannot request your own donation.")
        return redirect("donation_list")
    if not request.user.is_receiver:
        messages.error(request, "Only receivers can request donations.")
        return redirect("donation_list")
    if donation.available_till < timezone.now():
        donation.status = Donation.Status.EXPIRED
        donation.save(update_fields=["status"])
        messages.warning(request, "This donation has expired.")
        return redirect("donation_list")
    if request.method == "POST":
        form = FoodRequestForm(request.POST)
        if form.is_valid():
            food_request, created = FoodRequest.objects.get_or_create(
                donation=donation, receiver=request.user
            )
            if created:
                messages.success(request, "Request sent to donor.")
            else:
                messages.info(request, "You have already requested this item.")
            return redirect("request_list")
    else:
        form = FoodRequestForm()
    return render(request, "requests/form.html", {"form": form, "donation": donation})


@login_required
def request_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_donor:
        requests_qs = FoodRequest.objects.filter(donation__donor=request.user).select_related(
            "donation", "receiver"
        )
    else:
        requests_qs = FoodRequest.objects.filter(receiver=request.user).select_related("donation")
    return render(request, "requests/list.html", {"requests": requests_qs})


@login_required
@require_POST
def update_request_status(request: HttpRequest, pk: int) -> HttpResponse:
    food_request = get_object_or_404(FoodRequest, pk=pk, donation__donor=request.user)
    action = request.POST.get("action")
    if action == "accept":
        food_request.status = FoodRequest.Status.ACCEPTED
        food_request.save(update_fields=["status"])
        food_request.donation.status = Donation.Status.CLAIMED
        food_request.donation.save(update_fields=["status"])
        FoodRequest.objects.filter(
            donation=food_request.donation,
            status=FoodRequest.Status.PENDING,
        ).exclude(pk=food_request.pk).update(status=FoodRequest.Status.REJECTED)
        messages.success(request, "Request accepted. Donation marked as claimed.")
    elif action == "reject":
        food_request.status = FoodRequest.Status.REJECTED
        food_request.save(update_fields=["status"])
        messages.info(request, "Request rejected.")
    else:
        messages.error(request, "Invalid action.")
    return redirect("dashboard")
