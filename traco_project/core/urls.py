from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blogs/", views.blogs, name="blogs"),
    path("partner/", views.partner, name="partner"),
    path("partner/verify/<uuid:token>/", views.partner_verify, name="partner-verify"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
path("footer/subscribe/", views.footer_subscribe, name="footer_subscribe"),
    # working "Forgot your password?" link
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="auth/password_reset_form.html"
    ), name="password_reset"),
]
