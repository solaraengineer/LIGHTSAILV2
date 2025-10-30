from requests import Request

from logic.models import *
from django.views.decorators.http import require_GET
from django.http import JsonResponse, Http404
from logic.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django_ratelimit.decorators import ratelimit
import requests
from logic.forms import RegistrationForm, LoginForm, UpdateForm


@ratelimit(key='ip', rate='5/m', block=True)
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd["email"]
            password = cd["password"]

            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                auth_login(request, user)

                return redirect('dash')
            else:
                messages.error(request, "Invalid credentials", extra_tags="login")
                return render(request, "index.html", {"login_form": form, "reg_form": RegistrationForm()})

    return render(request, "index.html", {"login_form": form, "reg_form": RegistrationForm()})


ratelimit(key='ip', rate='5/m', block=True)
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get("username")
            email = cd.get("email")
            password = cd.get("password")

            recaptcha_token = request.POST.get("g-recaptcha-response")
            verify_url = "https://www.google.com/recaptcha/api/siteverify"
            payload = {
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": recaptcha_token,
            }

            try:
                response = requests.post(verify_url, data=payload, timeout=5)
                result = response.json()
            except Exception as e:
                messages.error(request, "Error verifying reCAPTCHA. Try again.", extra_tags="register")
                return render(request, "index.html", {"reg_form": form, "login_form": LoginForm()})

            if not result.get("success"):
                messages.error(request, "reCAPTCHA validation failed.", extra_tags="register")
                return render(request, "index.html", {"reg_form": form, "login_form": LoginForm()})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.", extra_tags="register")
                return render(request, "index.html", {"reg_form": form, "login_form": LoginForm()})

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.", extra_tags="register")
                return render(request, "index.html", {"reg_form": form, "login_form": LoginForm()})

            user = User(username=username, email=email)
            if form.cleaned_data.get("is_company"):
                user.account_type = "Firma"
            else:
                user.account_type = "User"

            user.set_password(password)
            user.save()

            auth_login(request, user)
            messages.success(request, "Account created successfully!", extra_tags="register")
            return redirect('dash')
        else:
            messages.error(request, "Please fix the errors below.", extra_tags="register")
            return render(request, "index.html", {"reg_form": form, "login_form": LoginForm()})
    else:
        form = RegistrationForm()

    return render(request, "index.html", {"reg_form": form, "login_form": LoginForm()})


def map(request):
    return render(request, "map.html", {
        "reg_form": RegistrationForm(),
        "login_form": LoginForm(),
    })

def dash(request):
    user = request.user
    if user.is_authenticated:
        return render(request, "dash.html", {
            "update_form": UpdateForm(),
            "username": user.username,
            "email": user.email,
        })
    return redirect('home')


def home(request):
    return render(request, "index.html", {
        "reg_form": RegistrationForm(),
        "login_form": LoginForm(),
    })

def info(request):
    user = request.user
    username = user.username if user.is_authenticated else None
    email = user.email if user.is_authenticated else None

    return render(request, "info.html", {
        "username": username,
        "email": email,
    })

def Update(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if cd.get("username") and cd["username"].strip():
                user.username = cd["username"].strip()

            if cd.get("email") and cd["email"].strip():
                user.email = cd["email"].strip()

            if cd.get("first_name") and cd["first_name"].strip():
                user.first_name = cd["first_name"].strip()

            if cd.get("last_name") and cd["last_name"].strip():
                user.last_name = cd["last_name"].strip()

            if cd.get("city") and cd["city"].strip():
                user.city = cd["city"].strip()

            if cd.get("address") and cd["address"].strip():
                user.address = cd["address"].strip()

            if cd.get("country") and cd["country"].strip():
                user.country = cd["country"].strip()

            if cd.get("password") and cd["password"].strip():
                user.set_password(cd["password"].strip())

            user.save()
            return redirect('dash')
    else:
        form = UpdateForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'city': user.city,
            'address': user.address,
        })

    return render(request, 'dash.html', {'form': form})

@require_GET
def house_detail(request, id_fme: str):
    try:
        h = House.objects.get(id_fme=id_fme)
    except House.DoesNotExist:
        raise Http404("House not found")
    return JsonResponse({
        "id": str(h.id),
        "id_fme": h.id_fme,
        "name": h.name,
        "status": h.status,
        "levels": float(h.fme_levels) if h.fme_levels is not None else None,
        "height": float(h.fme_height) if h.fme_height is not None else None,
        "h3_res": h.h3_res,
        "h3_id": h.h3_id,
        "created_at": h.created_at.isoformat() if h.created_at else None,
        "attrs": h.attrs,
    })


@require_GET
def house_detail(request, id_fme: str):
    try:
        h = House.objects.get(id_fme=id_fme)
    except House.DoesNotExist:
        raise Http404("House not found")
    return JsonResponse({
        "id": str(h.id),
        "id_fme": h.id_fme,
        "name": h.name,
        "status": h.status,
        "levels": float(h.fme_levels) if h.fme_levels is not None else None,
        "height": float(h.fme_height) if h.fme_height is not None else None,
        "h3_res": h.h3_res,
        "h3_id": h.h3_id,
        "created_at": h.created_at.isoformat() if h.created_at else None,
        "attrs": h.attrs,
    })