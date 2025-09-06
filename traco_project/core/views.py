from django.shortcuts import render
from django.shortcuts import render
from .models import HomePage, HomeFeature

# core/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import HomePage, HomeSectionCard

from .models import HowItWorks,CommunitySection,Banner

def _highlight_line(full: str, start: str | None, end: str | None) -> str:
    """
    Safely create HTML for a line that highlights `start` (first occurrence)
    and `end` (last occurrence). Returns plain string (not marked safe).
    """
    if not full:
        return ""

    result = full

    # highlight the first occurrence of start
    if start:
        try:
            if start in result:
                result = result.replace(start, f"<span class='neon-strong'>{start}</span>", 1)
        except Exception:
            pass

    # highlight the last occurrence of end
    if end:
        try:
            if end in result:
                parts = result.rsplit(end, 1)
                result = parts[0] + f"<span class='neon-strong'>{end}</span>" + parts[1]
        except Exception:
            pass

    return result

def home(request):
    page = HomePage.objects.first()
    features = HomeFeature.objects.all()
    cards_section = HomeSectionCard.objects.all().order_by("order", "serial")
    section = HowItWorks.objects.first()
    community_section = CommunitySection.objects.first()
    banner = Banner.objects.first()



    # Prepare HTML for lines with highlights (preserves your existing logic)
    if page:
        line3_html = _highlight_line(
            page.line3 or "",
            page.line3_highlight_start or "",
            page.line3_highlight_end or ""
        )
        line4_html = _highlight_line(
            page.line4 or "",
            page.line4_highlight_start or "",
            page.line4_highlight_end or ""
        )

        line3_html = mark_safe(line3_html)
        line4_html = mark_safe(line4_html)
    else:
        line3_html = ""
        line4_html = ""

    return render(request, "home.html", {
        "banner": banner,
        "page": page,
        "cards_section": cards_section,
        "features": features,   # keep the key name if your templates use 'features'; else use 'cards'
        "line3_html": line3_html,
        "line4_html": line4_html,
        "how_section": section,
        "community_section": community_section,
        "active_page": "home",
    })




from django.shortcuts import render
from .models import AboutPage, MissionVision, WhyChoose

def about(request):
    about_page = AboutPage.objects.first()
    mission = MissionVision.objects.filter(section_type="mission").first()
    vision = MissionVision.objects.filter(section_type="vision").first()
    why_choose = WhyChoose.objects.all()
    
    return render(request, "about.html", {
        "about_page": about_page,
        "mission": mission,
        "vision": vision,
        "why_choose": why_choose,
        "active_page": "about"
    })



def partner(request):
    return render(request, "navbar.html", {"active_page": "partner"})


# blog view

from django.db.models import Prefetch
from django.shortcuts import render
from .models import BlogHero, BlogCategory, BlogPost

def blogs(request):
    hero = BlogHero.objects.first()

    active_posts_qs = BlogPost.objects.filter(is_active=True).order_by('-published_on')
    categories = BlogCategory.objects.all().prefetch_related(
        Prefetch('posts', queryset=active_posts_qs, to_attr='active_posts')
    )

    active_slug = categories[0].slug if categories else ""
    return render(request, "blogs.html", {
        "hero": hero,
        "categories": categories,
        "active_slug": active_slug,
        "active_page": "blogs",
    })


# login/regitser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, LoginForm
from .models import AuthSideImage, UserProfile

def _side_image(page):
    try:
        return AuthSideImage.objects.get(page=page, active=True)
    except AuthSideImage.DoesNotExist:
        return None

def login_view(request):
    side = _side_image("login")
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].lower()
        pwd   = form.cleaned_data["password"]
        if not User.objects.filter(username=email).exists():
            messages.error(request, "User not found — register first.")
            return redirect("register")
        user = authenticate(request, username=email, password=pwd)
        if user is None:
            messages.error(request, "Incorrect password.")
        else:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")

    return render(request, "auth/login.html", {
        "form": form, "side": side, "active_page": "profile"
    })

def register_view(request):
    side = _side_image("register")
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # ✅ safe to access cleaned_data
            name   = form.cleaned_data["name"].strip()
            mobile = form.cleaned_data["mobile"]
            email  = form.cleaned_data["email"].lower()
            pwd    = form.cleaned_data["password1"]

            if User.objects.filter(username=email).exists():
                messages.warning(request, "User already exists — try to login.")
                return redirect("login")

            user = User.objects.create_user(username=email, email=email, first_name=name)
            user.set_password(pwd)
            user.save()
            UserProfile.objects.create(user=user, mobile=mobile)
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")

        else:
            # ❌ form invalid → pass errors to UI
            print("Form errors:", form.errors.as_json())  # for debugging
            messages.error(request, "Please fix the errors below.")

    return render(request, "auth/register.html", {
        "form": form,
        "side": side,
        "active_page": "profile",
    })


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("home")


# partner page
# views.py (updated partner view)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string

from .models import PartnerPage, PartnerFeature, PartnerApplication
from .forms import PartnerApplyForm


from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string

def partner(request):
    page = PartnerPage.objects.first()
    features = PartnerFeature.objects.all()

    # Prefill name/email for logged-in users (optional)
    initial = {}
    if request.user.is_authenticated:
        if request.user.first_name:
            initial["name"] = request.user.first_name
        if request.user.email:
            initial["email"] = request.user.email

    # If a message was stored in the session by a previous POST+redirect, pop it
    messagealert = request.session.pop('messagealert', '')

    form = PartnerApplyForm(initial=initial)

    if request.method == "POST":
        # require login
        if not request.user.is_authenticated:
            request.session['messagealert'] = "Please login to continue."
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        form = PartnerApplyForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.otp = get_random_string(6, allowed_chars="0123456789")
            app.save()

            # Build verify URL
            verify_url = request.build_absolute_uri(f"/partner/verify/{app.token}/")

            # Recipients: applicant + team/default mailbox
            team_email = getattr(settings, "PARTNER_TEAM_EMAIL",
                                 getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@traco.local"))
            recipients = [app.email, team_email]

            subject = "TRACO Partner – Verify your request"
            text_body = (
                f"Hi {app.name},\n\n"
                f"Your OTP is: {app.otp}\n\n"
                f"Click the link below to become a partner:\n{verify_url}\n\n"
                "If you did not request this, please ignore this email."
            )
            html_body = f"""
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#111">
                  <p>Hi <strong>{app.name}</strong>,</p>
                  <p>Your OTP is:</p>
                  <p style="font-size:22px;font-weight:800;letter-spacing:2px;margin:8px 0">
                    {app.otp}
                  </p>
                  <p>
                    Click the link below to become a partner:<br>
                    <a href="{verify_url}" target="_blank"
                       style="color:#2b7cff;text-decoration:none">{verify_url}</a>
                  </p>
                  <p style="color:#555">If you did not request this, please ignore this email.</p>
                </div>
            """

            try:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_body,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@traco.local"),
                    to=recipients,
                )
                email.attach_alternative(html_body, "text/html")
                email.send(fail_silently=False)
                request.session['messagealert'] = "OTP and verification link sent to your email."
            except Exception as e:
                # store the real exception text (safe for dev — consider hiding details in production)
                request.session['messagealert'] = f"Could not send email. {e}"

            return redirect("partner")

        else:
            request.session['messagealert'] = "Please correct the errors and submit again."
            # keep the bound form and redirect so the message is shown.
            # If you prefer to show errors inline without redirect, remove this redirect and fall through to render()
            return redirect("partner")

    # GET or non-redirect render
    return render(request, "partner.html", {
        "messagealert": messagealert,
        "page": page,
        "features": features,
        "form": form,
        "active_page": "partner",
    })



def partner_verify(request, token):
    app = get_object_or_404(PartnerApplication, token=token)
    app.status = "verified"
    app.save(update_fields=["status"])
    messages.success(request, "You are now a partner of TRACO!")
    return redirect("partner")


# footer view
import re
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import FooterSettings, NewsletterSubscriber

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")  # basic email validation

@require_POST
def footer_subscribe(request):
    """
    AJAX endpoint to subscribe user to newsletter.
    Expects POST { email: "..." } and returns JSON.
    """
    email = request.POST.get("email", "").strip()
    # Validate: must match regex and must include ".com" and '@' (user requested that)
    if not email or not EMAIL_REGEX.match(email) or ".com" not in email:
        return JsonResponse({"ok": False, "error": "Please provide a valid email address (must include @ and .com)."}, status=400)

    # Save subscriber (unique constraint on email)
    created = False
    try:
        obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
    except Exception as e:
        return JsonResponse({"ok": False, "error": "Could not save subscription. Try again later."}, status=500)

    # Send notification email to configured recipient if available, else to DEFAULT_FROM_EMAIL
    try:
        footer = FooterSettings.objects.first()
        notify_to = None
        if footer and footer.newsletter_subscriber_notify_email:
            notify_to = footer.newsletter_subscriber_notify_email
        else:
            # fallback to settings.DEFAULT_FROM_EMAIL if present
            notify_to = getattr(settings, "DEFAULT_FROM_EMAIL", None)

        subject = "New Newsletter Subscription"
        body = f"New subscriber: {email}\n\nFrom site: {request.get_host()}"
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "no-reply@localhost"

        if notify_to:
            send_mail(subject, body, from_email, [notify_to], fail_silently=False)
    except Exception:
        # Do not reveal mail issues to user; still return success (or partial)
        pass

    return JsonResponse({"ok": True, "message": "Thank you for subscribing to TRACO! Check your inbox."})
