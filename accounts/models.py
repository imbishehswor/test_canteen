from asyncio.windows_events import NULL
import email
from pyexpat import model
from django.db import models

# Create your models here.
class Users(models.Model):
    # user_id = models.BigAutoField(primary_key=True)
    user_fullname = models.CharField(max_length=100) 
    user_phone = models.CharField(max_length=10)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=20)
    user_role = models.BooleanField()

    class Meta:
        db_table = "users"