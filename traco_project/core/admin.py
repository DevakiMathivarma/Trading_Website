from django.contrib import admin
from .models import AboutPage, MissionVision, WhyChoose

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ["banner_title"]

@admin.register(MissionVision)
class MissionVisionAdmin(admin.ModelAdmin):
    list_display = ["title", "section_type"]

@admin.register(WhyChoose)
class WhyChooseAdmin(admin.ModelAdmin):
    list_display = ["title"]


# blog page
from django.contrib import admin
from .models import BlogHero, BlogCategory, BlogPost

@admin.register(BlogHero)
class BlogHeroAdmin(admin.ModelAdmin):
    list_display = ("heading_line", "highlight_text", "oval_width", "oval_height")
    fieldsets = (
        (None, {"fields": ("heading_line", "highlight_text", "subtext")}),
        ("Hero Image", {"fields": ("image", "oval_width", "oval_height")}),
    )

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order",)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_on", "read_minutes", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "overlay_title")
    date_hierarchy = "published_on"


# login/register
from django.contrib import admin
from .models import AuthSideImage, UserProfile

@admin.register(AuthSideImage)
class AuthSideImageAdmin(admin.ModelAdmin):
    list_display = ("page", "active")
    list_editable = ("active",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile")

# partner page
from django.contrib import admin
from .models import PartnerPage, PartnerCity, PartnerFeature, PartnerApplication

@admin.register(PartnerPage)
class PartnerPageAdmin(admin.ModelAdmin):
    list_display = ("highlight", "email_value", "phone_value")

@admin.register(PartnerCity)
class PartnerCityAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order",)

@admin.register(PartnerFeature)
class PartnerFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(PartnerApplication)
class PartnerApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "city", "status", "created_at")
    list_filter = ("status", "city")
    search_fields = ("name", "email", "phone")

# homepage
from django.contrib import admin
from .models import HomePage, HomeFeature

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

@admin.register(HomeFeature)
class HomeFeatureAdmin(admin.ModelAdmin):
    list_display = ("order", "title_part_left", "title_highlight", "title_part_right")
    ordering = ("order",)

from django.contrib import admin
from .models import HomeSectionCard

@admin.register(HomeSectionCard)
class HomeSectionCardAdmin(admin.ModelAdmin):
    list_display = ("serial", "title", "is_center", "order")
    list_editable = ("is_center", "order")
    fields = ("serial", "title", "subtitle", "description", "link", "is_center", "order")
    ordering = ("order", "serial")


from django.contrib import admin
from .models import HowItWorks, HowItWorksStep

class HowItWorksStepInline(admin.TabularInline):
    model = HowItWorksStep
    fields = ("order", "title", "description", "icon", "accent_color")
    extra = 0
    ordering = ("order",)
    readonly_fields = ()

@admin.register(HowItWorks)
class HowItWorksAdmin(admin.ModelAdmin):
    inlines = (HowItWorksStepInline,)
    list_display = ("__str__",)

@admin.register(HowItWorksStep)
class HowItWorksStepAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "section")
    list_filter = ("section",)
    ordering = ("section", "order")


# footer
from django.contrib import admin
from .models import FooterSettings, SocialLink, FooterLink, NewsletterSubscriber

@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "newsletter_subscriber_notify_email")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order")
    ordering = ("order",)


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("column", "text", "url", "order")
    list_filter = ("column",)
    ordering = ("column", "order")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "confirmed")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


# community
from django.contrib import admin
from .models import CommunitySection, CommunityImage   # ✅ Import both models


class CommunityImageInline(admin.TabularInline):       # ✅ Inline for images
    model = CommunityImage
    extra = 5
    fields = ("order", "image", "caption")
    ordering = ("order",)


@admin.register(CommunitySection)
class CommunitySectionAdmin(admin.ModelAdmin):
    inlines = (CommunityImageInline,)
    list_display = ("__str__", "heading_before", "heading_strong", "heading_after")
    fields = (
        "hero_image", "hero_image_alt",
        "heading_before", "heading_strong", "heading_after",
        "line_1", "line_2", "line_3", "caption",
    )

from django.contrib import admin
from .models import Banner, BannerAvatar, CTA

class BannerAvatarInline(admin.TabularInline):
    model = BannerAvatar
    extra = 3
    fields = ("image", "alt", "order")

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "title_small", "created")
    inlines = (BannerAvatarInline,)
    ordering = ("-created",)
    fieldsets = (
        (None, {
            "fields": ("title_small", "title_line1", "title_line2", "title_line3",
                       "background_image", "man_image", "user_count_text", "user_count_label")
        }),
    )

@admin.register(CTA)
class CTAAdmin(admin.ModelAdmin):
    list_display = ("banner", "label")

