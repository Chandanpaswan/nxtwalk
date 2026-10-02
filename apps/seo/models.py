from django.db import models


class SEOFields(models.Model):
    seo_title = models.CharField(max_length=60, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    keywords = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        abstract = True