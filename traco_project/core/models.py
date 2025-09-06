from django.db import models

class AboutPage(models.Model):
    banner_image = models.ImageField(upload_to="about/")
    banner_title = models.CharField(max_length=200, default="About TRACO")
    who_we_are_title = models.CharField(max_length=100, default="Who are We?")
    who_we_are_text1 = models.TextField()
    who_we_are_text2 = models.TextField()

    def __str__(self):
        return "About Page Content"


class MissionVision(models.Model):
    SECTION_CHOICES = [
        ("mission", "Mission"),
        ("vision", "Vision"),
    ]
    section_type = models.CharField(max_length=10, choices=SECTION_CHOICES)
    image = models.ImageField(upload_to="about/")
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class WhyChoose(models.Model):
    icon = models.ImageField(upload_to="about/")
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


# blog page
from django.db import models

class BlogHero(models.Model):
    heading_line = models.CharField(max_length=120, default="Don’t Just Gain info")
    highlight_text = models.CharField(max_length=50, default="Build Knowledge")
    subtext = models.TextField(
        default="Whether you’re a new investor or a market expert, we’ve got something for everyone at the <span class='neon'>TRACO</span> blog"
    )
    image = models.ImageField(upload_to="blogs/hero/")
    # oval sizes to control exact replica from admin
    oval_width = models.PositiveIntegerField(default=260)
    oval_height = models.PositiveIntegerField(default=320)

    def __str__(self):
        return "Blogs Hero"

class BlogCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="blogs/posts/")
    overlay_title = models.CharField(max_length=80)          # text on the image
    title = models.CharField(max_length=140)                 # text below card image
    read_minutes = models.PositiveIntegerField(default=5)
    published_on = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_on"]

    def __str__(self):
        return self.title

    @property
    def meta_text(self):
        # e.g. "5 Mins Read · 20 May 2025"
        return f"{self.read_minutes} Mins Read · {self.published_on.strftime('%d %b %Y')}"


# login/register
from django.db import models
from django.contrib.auth.models import User

class AuthSideImage(models.Model):
    PAGE_CHOICES = (("login", "Login"), ("register", "Register"))
    page = models.CharField(max_length=10, choices=PAGE_CHOICES, unique=True)
    image = models.ImageField(upload_to="auth_side/")
    alt_text = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_page_display()} Image"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# partner page
from django.db import models
from django.contrib.auth.models import User
import uuid

class PartnerPage(models.Model):
    # hero / header
    hero_image = models.ImageField(upload_to="partner/hero/")
    heading_lead = models.CharField(max_length=120, default="Welcome to the First Step of Becoming a")
    highlight = models.CharField(max_length=32, default="TRACO")
    heading_tail = models.CharField(max_length=32, default="Partner")
    # contact
    contact_heading = models.CharField(max_length=120, default="Contact us Alternatively , You can Contact Our Business Partner Team")
    phone_label = models.CharField(max_length=64, default="Phone Number")
    phone_value = models.CharField(max_length=64, default="022 982231")
    email_label = models.CharField(max_length=64, default="Email id")
    email_value = models.EmailField(default="businesspartner@tranco.in")

    # center copy
    line1 = models.CharField(max_length=200, default="People become partners to earn passive income and grow with a trusted brand.")
    line2 = models.CharField(max_length=220, default="They get access to high commissions, marketing support, and long-term business potential.")
    line3 = models.CharField(max_length=120, blank=True, default="")

    def __str__(self):
        return "Partner Page"

class PartnerCity(models.Model):
    name = models.CharField(max_length=60, unique=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

class PartnerFeature(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    icon = models.ImageField(upload_to="partner/features/")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class PartnerApplication(models.Model):
    STATUS = (("pending", "Pending"), ("verified", "Verified"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partner_apps")
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.ForeignKey(PartnerCity, on_delete=models.PROTECT)
    pincode = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.city} - {self.status}"


# homepage
from django.db import models

class HomePage(models.Model):
    # large number graphic (you can upload '20' rendered image) OR site will render large numeric CSS if left empty
    number_image = models.ImageField(upload_to="home/hero/", blank=True, null=True)
    right_hero_image = models.ImageField(upload_to="home/hero/", blank=True, null=True)

    # paragraph lines (we keep plain text and template wraps highlights)
    line1 = models.TextField(default="20 years of industry expertise, we've empowered thousands")
    line2 = models.TextField(default="of traders to take control of their financial future. Our platform")
    line3 = models.TextField(default="combines proven experience with cutting-edge tools to help")
    line4 = models.TextField(default="you trade smarter, faster, and more confidently.")

    # styled words (so template can color the start/ends exactly)
    # we will highlight the start word(s) and end word(s) with neon
    # for simplicity, store start & end words for line3 and line4 or leave blank
    line3_highlight_start = models.CharField(max_length=60, blank=True, default="combines")
    line3_highlight_end = models.CharField(max_length=60, blank=True, default="tools")
    line4_highlight_start = models.CharField(max_length=60, blank=True, default="you trade smarter,")
    line4_highlight_end = models.CharField(max_length=60, blank=True, default="confidently")

    # the left/middle/right feature blocks are modeled below:
    def __str__(self):
        return "Home Page content (single entry)"

class HomeFeature(models.Model):
    order = models.PositiveIntegerField(default=1)
    # parts so we can color words separately in template
    title_part_left = models.CharField(max_length=100, blank=True, help_text="left part (colored green)")
    title_part_right = models.CharField(max_length=100, blank=True, help_text="right part (colored green)")
    title_highlight = models.CharField(max_length=100, blank=True, help_text="TRACO or main highlight (radial color)")
    subtitle = models.TextField(blank=True, help_text="small paragraph / lines")
    icon = models.ImageField(upload_to="home/features/", blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title_part_left} {self.title_highlight} {self.title_part_right}"

from django.db import models
from django.urls import reverse, NoReverseMatch

class HomeSectionCard(models.Model):
    SERIAL_CHOICES = [
        (1, "01"),
        (2, "02"),
        (3, "03"),
    ]

    serial = models.PositiveSmallIntegerField(choices=SERIAL_CHOICES, unique=True)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    link = models.CharField(
        max_length=255,
        blank=True,
        help_text="Either a path (/blogs/) or a named URL (blogs). First & second cards will link to {% url 'blogs' %} in template."
    )
    is_center = models.BooleanField(default=False, help_text="Make this the taller neon center card")
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers show first (left)")

    class Meta:
        ordering = ["order", "serial"]
        verbose_name = "Home Section Card"
        verbose_name_plural = "Home Section Cards"

    def __str__(self):
        return f"{self.get_serial_display()} — {self.title}"

    def get_link(self):
        """
        Return a usable URL. If link looks like a path or absolute URL return it.
        If it's a named URL attempt to reverse it; otherwise fallback to '#'.
        """
        if not self.link:
            return "#"
        if self.link.startswith("/") or self.link.startswith("http"):
            return self.link
        try:
            return reverse(self.link)
        except NoReverseMatch:
            return self.link


# wave like 
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator

class HowItWorks(models.Model):
    """
    Single top-level record containing section title and optional background image.
    Keep only one instance (get via .first() in view).
    """
    title = models.CharField(max_length=120, default="How it Works?")
    background = models.ImageField(upload_to="how/bg/", blank=True, null=True,
                                   help_text="Optional subtle background or pattern (not required)")

    def __str__(self):
        return "How it Works section"

class HowItWorksStep(models.Model):
    """
    Steps ordered left → right. Each step has icon (image), title, description and order.
    """
    section = models.ForeignKey(HowItWorks, related_name="steps", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0)])
    title = models.CharField(max_length=80)
    description = models.TextField(help_text="Short paragraph shown under the title")
    icon = models.ImageField(upload_to="how/icons/", blank=False, null=False)
    # optional small accent color override (defaults to neon)
    accent_color = models.CharField(max_length=7, default="#a7f542", help_text="Hex color (e.g. #a7f542)")

    class Meta:
        ordering = ("order",)
        verbose_name = "How it Works step"

    def __str__(self):
        return f"{self.order} - {self.title}"


# footer
from django.db import models
from django.utils import timezone

class FooterSettings(models.Model):
    """
    Singleton-ish model to hold global footer settings (logo, newsletter recipient, small texts).
    Create one record in admin.
    """
    site_logo = models.ImageField(upload_to="footer/", blank=True, null=True)
    logo_alt = models.CharField(max_length=120, blank=True, default="TRACO")
    newsletter_heading = models.CharField(max_length=120, default="Newsletter")
    newsletter_placeholder = models.CharField(max_length=120, default="Enter Your Email")
    newsletter_button_text = models.CharField(max_length=60, default="Subscribe")
    newsletter_subscriber_notify_email = models.EmailField(
        blank=True,
        help_text="Email that receives subscription notifications (optional)."
    )
    newsletter_description = models.TextField(
        blank=True,
        default="NFT's are Transforming the way Commerce is a Transacted."
    )

    def __str__(self):
        return "Footer Settings"

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"


class SocialLink(models.Model):
    """
    Social icons shown under logo. Icon_type is one of 'facebook','twitter','instagram'.
    Admin sets URL and order.
    """
    ICON_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
    ]
    name = models.CharField(max_length=30, choices=ICON_CHOICES)
    url = models.URLField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.get_name_display()} -> {self.url}"


class FooterLink(models.Model):
    """
    Individual footer links. Use column 1..5 to distribute across 5 columns.
    """
    COLUMN_CHOICES = [(i, f"Column {i}") for i in range(1, 6)]
    column = models.PositiveSmallIntegerField(choices=COLUMN_CHOICES, default=1)
    text = models.CharField(max_length=160)
    url = models.CharField(max_length=255, blank=True, help_text="External URL or site path")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["column", "order"]

    def __str__(self):
        return f"Col {self.column}: {self.text}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# community section
from django.db import models

# models.py (only the CommunitySection part shown)
from django.db import models

class CommunitySection(models.Model):
    heading_before = models.CharField(max_length=120, default="Build a")
    heading_strong = models.CharField(max_length=120, default="Strong")
    heading_after = models.CharField(max_length=120, default="Community")

    line_1 = models.CharField(max_length=240, blank=True, default="Join a global network of passionate traders.")
    line_2 = models.CharField(max_length=240, blank=True, default="Share strategies, learn from experts, and grow together")
    line_3 = models.CharField(max_length=240, blank=True, default="in a supportive, success-driven environment.")
    caption = models.CharField(max_length=300, blank=True)

    # NEW: hero image shown above the heading (rounded neon bordered frame)
    hero_image = models.ImageField(upload_to="community/hero/", blank=True, null=True)
    hero_image_alt = models.CharField(max_length=150, blank=True, default="Community Preview")

    def __str__(self):
        return "Community Section"



class CommunityImage(models.Model):
    """
    Individual images for the section. Use `order` to place them.
    We expect 5 images: first row 3 small images (order 1..3),
    second row 2 wide images (order 4..5). Images are uploaded from admin.
    """
    section = models.ForeignKey(CommunitySection, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="community/")
    caption = models.CharField(max_length=160, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image {self.order} for Community"




from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Banner(models.Model):
    """
    Single hero/banner model to manage the homepage banner content via admin.
    Keep one row (use .first() in views).
    """
    title_small = models.CharField(max_length=120, blank=True, help_text="Keep your money safe text")
    title_line1 = models.CharField(max_length=160, blank=True)
    title_line2 = models.CharField(max_length=160, blank=True)
    title_line3 = models.CharField(max_length=160, blank=True)
    background_image = models.ImageField(upload_to="banners/", blank=True, null=True)
    man_image = models.ImageField(upload_to="banners/", blank=True, null=True,
                                  help_text="Right-side man image (PNG recommended with transparent background if you want overlap).")
    # numbers + label
    user_count_text = models.CharField(max_length=64, default="500+")
    user_count_label = models.CharField(max_length=64, default="Realtime Users")

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banner ({self.pk})"

class BannerAvatar(models.Model):
    """
    Avatars shown overlapping below the heading. Use admin inline to add many.
    """
    banner = models.ForeignKey(Banner, related_name="avatars", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="banners/avatars/")
    alt = models.CharField(max_length=100, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.alt or f"Avatar {self.pk}"

class CTA(models.Model):
    """
    The circular overlapping CTA (two circles + arrow) is static design,
    but we keep a CTA model if you want to change label via admin.
    """
    banner = models.ForeignKey(Banner, related_name="ctas", on_delete=models.CASCADE)
    label = models.CharField(max_length=120, default="Your Trading Journey Started Here....")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

