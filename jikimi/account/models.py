from django.db import models
from django.contrib.auth.models import AbstractUser
from violence_data_page.models import School 

# Create your models here.

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    user_phone = models.CharField(unique=True, max_length=11, blank=True, null=True)
    user_school = models.ForeignKey(School, models.DO_NOTHING, db_column='user_school', blank=True, null=True)
    profile_img = models.ImageField(upload_to = "profile_img/", null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'User'
