import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator
from django.db import models
from apps.seo.models import SEOFields


class SiteSettings(models.Model):
    organization_name = models.CharField("company name", max_length=120, default="NXTWALK")
    tagline = models.CharField(max_length=180, default="Build. Grow. Walk Ahead.")
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    whatsapp_number = models.CharField(
        max_length=24,
        blank=True,
        validators=[RegexValidator(r"^\+?[0-9\s().-]{8,24}$", "Enter a valid WhatsApp number.")],
    )
    address = models.CharField(max_length=240, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    business_hours = models.CharField(max_length=240, blank=True)
    google_maps_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="site/", blank=True)
    favicon = models.FileField(upload_to="site/", blank=True)
    footer_description = models.CharField(max_length=240, default="Digital systems for the next generation.")
    default_seo_title = models.CharField(max_length=60, blank=True)
    default_meta_description = models.CharField(max_length=160, blank=True)
    default_keywords = models.TextField(blank=True)
    default_og_image = models.ImageField(upload_to="site/", blank=True)
    google_analytics_id = models.CharField(max_length=40, blank=True)
    search_console_verification = models.CharField(max_length=160, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @property
    def company_name(self):
        return self.organization_name

    @property
    def whatsapp_link(self):
        digits = re.sub(r"\D", "", self.whatsapp_number)
        return f"https://wa.me/{digits}" if 8 <= len(digits) <= 15 else ""

    def __str__(self):
        return self.organization_name


class SocialLink(models.Model):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    X = "x"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    WHATSAPP = "whatsapp"
    OTHER = "other"
    PLATFORM_CHOICES = [
        (INSTAGRAM, "Instagram"),
        (FACEBOOK, "Facebook"),
        (X, "X"),
        (LINKEDIN, "LinkedIn"),
        (YOUTUBE, "YouTube"),
        (WHATSAPP, "WhatsApp"),
        (OTHER, "Other"),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    name = models.CharField(max_length=80)
    url = models.URLField(validators=[URLValidator(schemes=["https", "http"])])
    icon = models.CharField(max_length=20, choices=PLATFORM_CHOICES, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_new_tab = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def save(self, *args, **kwargs):
        if not self.icon:
            self.icon = self.platform
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FooterSettings(models.Model):
    logo = models.ImageField(upload_to="site/", blank=True)
    description = models.CharField(max_length=240, default="Digital systems for the next generation.")
    copyright_text = models.CharField(max_length=180, blank=True)
    show_social_links = models.BooleanField(default=True)
    show_whatsapp = models.BooleanField(default=True)
    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=True)
    show_address = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "footer settings"
        verbose_name_plural = "footer settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Footer settings"


class FooterLink(models.Model):
    COMPANY = "company"
    SERVICES = "services"
    RESOURCES = "resources"
    SECTION_CHOICES = [
        (COMPANY, "Company"),
        (SERVICES, "Services"),
        (RESOURCES, "Resources"),
    ]

    section = models.CharField(max_length=16, choices=SECTION_CHOICES)
    title = models.CharField(max_length=80)
    url = models.CharField(max_length=300, blank=True, help_text="Internal path, starting with /")
    external_url = models.URLField(blank=True, validators=[URLValidator(schemes=["https", "http"])])
    is_external = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["section", "display_order", "id"]

    def clean(self):
        super().clean()
        if self.is_external:
            if not self.external_url:
                raise ValidationError({"external_url": "An external URL is required for external footer links."})
        elif not self.url.startswith("/") or self.url.startswith("//"):
            raise ValidationError({"url": "Internal URLs must be local paths beginning with a single /."})

    @property
    def href(self):
        return self.external_url if self.is_external else self.url

    def __str__(self):
        return f"{self.get_section_display()}: {self.title}"


class NavigationItem(models.Model):
    title = models.CharField(max_length=80)
    url = models.CharField(max_length=300, blank=True, help_text="Internal path, starting with /")
    external_url = models.URLField(blank=True, validators=[URLValidator(schemes=["https", "http"])])
    is_external = models.BooleanField(default=False)
    is_cta = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "id"]

    def clean(self):
        super().clean()
        if self.is_external:
            if not self.external_url:
                raise ValidationError({"external_url": "An external URL is required for external menu items."})
        elif not self.url.startswith("/") or self.url.startswith("//"):
            raise ValidationError({"url": "Internal URLs must be local paths beginning with a single /."})
        if self.is_cta and NavigationItem.objects.exclude(pk=self.pk).filter(is_cta=True).exists():
            raise ValidationError({"is_cta": "Only one navigation item can be the primary CTA."})

    @property
    def href(self):
        return self.external_url if self.is_external else self.url

    def __str__(self):
        return self.title


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email


class Page(SEOFields):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title