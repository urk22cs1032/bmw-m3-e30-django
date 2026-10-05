from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from showroom.forms import VehicleForm
from showroom.models import Vehicle



# ============================================================
# HOME
# ============================================================

def home(request):
    return render(request, "home.html")


# ============================================================
# COLLECTION
# ============================================================

def collection(request):

    vehicles = Vehicle.objects.all().order_by("-created_at")

    query = (request.GET.get("q") or "").strip()

    requested_status = (
        request.GET.get("status") or ""
    ).strip().upper()

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if query:
        vehicles = vehicles.filter(
            Q(bmw_id__icontains=query)
            | Q(model__icontains=query)
            | Q(variant__icontains=query)
            | Q(customer_name__icontains=query)
            | Q(registration_number__icontains=query)
        )

    # --------------------------------------------------------
    # STATUS FILTER
    # --------------------------------------------------------

    valid_statuses = {
        code
        for code, _label in Vehicle.Status.choices
    }

    if requested_status in valid_statuses:
        vehicles = vehicles.filter(
            status=requested_status
        )

        status = requested_status

    else:
        status = ""

    return render(
        request,
        "collection.html",
        {
            "vehicles": vehicles,
            "query": query,
            "status": status,
            "statuses": Vehicle.Status.choices,
        },
    )


# ============================================================
# VEHICLE DETAIL
# ============================================================

def vehicle_detail(request, pk):

    vehicle = get_object_or_404(
        Vehicle,
        pk=pk
    )

    return render(
        request,
        "vehicle_detail.html",
        {
            "vehicle": vehicle
        },
    )


# ============================================================
# ABOUT
# ============================================================

def about(request):

    return render(
        request,
        "about.html"
    )


# ============================================================
# MANAGEMENT
# ============================================================
@login_required
def management(request):

    vehicles = Vehicle.objects.all().order_by("-created_at")

    total_vehicles = Vehicle.objects.count()

    delivered = Vehicle.objects.filter(
        status="DELIVERED"
    ).count()

    in_process = Vehicle.objects.filter(
        status="IN_PROCESS"
    ).count()

    pending = Vehicle.objects.filter(
        status="PENDING"
    ).count()

    return render(
        request,
        "management.html",
        {
            "vehicles": vehicles,
            "total_vehicles": total_vehicles,
            "delivered": delivered,
            "in_process": in_process,
            "pending": pending,
        },
    )


# ============================================================
# ADD BMW VEHICLE
# ============================================================
@login_required
def vehicle_add(request):

    if request.method == "POST":

        form = VehicleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            # After adding the vehicle,
            # automatically go to BMW Collection.
            return redirect("collection")

    else:

        form = VehicleForm()

    return render(
        request,
        "vehicle_form.html",
        {
            "form": form,
            "page_title": "Add BMW Vehicle",
            "submit_text": "ADD BMW VEHICLE",
        },
    )


# ============================================================
# EDIT BMW VEHICLE
# ============================================================

@login_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(
        Vehicle,
        pk=pk
    )

    if request.method == "POST":

        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle
        )

        if form.is_valid():

            form.save()

            return redirect(
                "collection"
            )

    else:

        form = VehicleForm(
            instance=vehicle
        )

    return render(
        request,
        "vehicle_form.html",
        {
            "form": form,
            "vehicle": vehicle,
            "page_title": "Edit BMW Vehicle",
            "submit_text": "UPDATE BMW VEHICLE",
        },
    )


# ============================================================
# DELETE BMW VEHICLE
# ============================================================
@login_required
def vehicle_delete(request, pk):
    """Show a confirmation page, and delete only once that page is POSTed.

    Deleting on GET would let any link prefetch, browser speculation rule or
    crawler visit destroy the record, so the delete sits behind an explicit
    POST. The confirmation template names the record rather than saying "this
    item", so what is about to be lost is unambiguous.
    """

    vehicle = get_object_or_404(
        Vehicle,
        pk=pk
    )

    if request.method == "POST":

        # Held before the row goes, so the file removal below cannot be
        # affected by anything the delete does to the instance.
        image = vehicle.image

        vehicle.delete()

        # Django does NOT remove the file behind an ImageField when the row
        # goes. Without this, uploads/ grows without bound and keeps the photos
        # of records that no longer exist.
        if image:
            image.delete(save=False)

        return redirect(
            "collection"
        )

    return render(
        request,
        "vehicle_confirm_delete.html",
        {
            "vehicle": vehicle
        },
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def user_login(request):
    # If already logged in, go directly to management
    if request.user.is_authenticated:
        return redirect("management")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            # Login any valid registered user
            login(request, user)

            next_url = request.GET.get("next")

            if next_url and next_url.startswith("/"):
                return redirect(next_url)

            return redirect("management")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "registration/login.html"
    )


def user_logout(request):
    logout(request)
    return redirect("home")


def user_register(request):
    # Already logged-in users go to management
    if request.user.is_authenticated:
        return redirect("management")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not username:
            messages.error(request, "Username is required.")
            return render(
                request,
                "registration/register.html"
            )

        if not email:
            messages.error(request, "Email is required.")
            return render(
                request,
                "registration/register.html"
            )

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(
                request,
                "registration/register.html"
            )

        if not password1:
            messages.error(request, "Password is required.")
            return render(
                request,
                "registration/register.html"
            )

        if len(password1) < 8:
            messages.error(
                request,
                "Password must be at least 8 characters long."
            )
            return render(
                request,
                "registration/register.html"
            )

        from django.contrib.auth.models import User

        try:
            if User.objects.filter(
                username=username
            ).exists():

                messages.error(
                    request,
                    "Username already exists."
                )

                return render(
                    request,
                    "registration/register.html"
                )

            if User.objects.filter(
                email=email
            ).exists():

                messages.error(
                    request,
                    "Email already exists."
                )

                return render(
                    request,
                    "registration/register.html"
                )

            User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            messages.success(
                request,
                "Account created successfully. Please log in."
            )

            return redirect("login")

        except Exception:
            messages.error(
                request,
                "An error occurred while creating your account."
            )

            return render(
                request,
                "registration/register.html"
            )

    return render(
        request,
        "registration/register.html"
    )