from django.db import models


class CSVFile(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='csv_files/')

    def __str__(self):
        return self.name
