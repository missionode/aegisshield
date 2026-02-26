from django.db import models
from django.conf import settings

class Disease(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    immediate_action = models.TextField()
    long_term_care = models.TextField()
    recommended_products = models.JSONField(default=list) # List of dicts: {name, price, icon}

    def __str__(self):
        return self.name

class Scan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scans')
    image = models.ImageField(upload_to='scans/')
    date = models.DateTimeField(auto_now_add=True)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    confidence = models.FloatField(default=0.0)
    raw_ai_response = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Scan {self.id} - {self.user.username}"