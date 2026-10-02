from django.db import models
from apps.seo.models import SEOFields


class CaseStudy(SEOFields):
    project = models.OneToOneField("portfolio.Project", on_delete=models.CASCADE, related_name="case_study")
    industry = models.CharField(max_length=120)
    strategy = models.TextField()
    implementation = models.TextField()
    technology = models.TextField(blank=True)
    seo_strategy = models.TextField(blank=True)
    marketing_strategy = models.TextField(blank=True)
    results = models.TextField()
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "project__title"]

    def __str__(self):
        return f"{self.project.title} case study"