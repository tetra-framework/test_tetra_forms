from django.db import models
from django.contrib.auth.models import Group


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, default=None)
    attachment = models.FileField(upload_to="files/", null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}; Group: {self.group}"

    def delete(self, using=None, keep_parents=False):
        # Delete the person's attachment file if it exists before deleting the person itself.
        if self.attachment:
            self.attachment.delete()
        super().delete(using, keep_parents)
