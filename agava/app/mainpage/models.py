from django.db import models
from django.urls import reverse


class MainPageDocumentationModel(models.Model):
    title = models.CharField(max_length=200, help_text="title", null=True)
    doc_content = models.TextField(help_text="content", null=True)

    def get_absolute_url(self):
        return reverse('doc_detail', kwargs={'id': self.id})

