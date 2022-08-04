from django.db import models
import uuid

#uuid, email, provider, username, birth
class User(models.Model):
    uuid=models.UUIDField(
        #primary_key=True,
        default=uuid.uuid4,
        unique=True,
        db_index=True,
    )
    email=models.EmailField(
        verbose_name=('email'),
        max_length=64,
        unique=True,
        null=False,
        blank=False,
    )
    username=models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    provider=models.CharField(
        max_length=20,
        null=False,
        blank=False,
    )
    birth=models.DateField(
        blank=True,
    )

    def __str__(self):
        return str(self.uuid)
    
    def get_email(self):
        return str(self.email)
