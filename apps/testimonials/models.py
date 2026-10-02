from django.db import models


class Testimonial(models.Model):
    client_name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=180, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} - {self.company}".strip(" -")