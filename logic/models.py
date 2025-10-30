from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True,)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=255,  blank=False, default="")
    first_name = models.CharField(max_length=150, blank=False, default="")
    last_name = models.CharField(max_length=150,blank=False, default="")
    city = models.CharField(max_length=150, blank=False, default="")
    address = models.CharField(max_length=150, blank=False, default="")
    country = models.CharField(max_length=150, blank=False, default="")
    referral = models.CharField(max_length=150, blank=False, default="")
    account_type = models.CharField(max_length=150, blank=False, default="")

class FA(models.Model):
    user_id = models.CharField(unique=True,)
    code = models.CharField(max_length=6, null=False, blank=False)

class House(models.Model):
        id = models.UUIDField(primary_key=True, db_column='id')
        owner_id = models.UUIDField(db_column='owner_id', null=True, blank=True)
        address_id = models.UUIDField(db_column='address_id', null=True, blank=True)

        status = models.TextField(db_column='status', null=True, blank=True)
        attrs = models.JSONField(db_column='attrs', null=True, blank=True)

        created_at = models.DateTimeField(db_column='created_at', null=True, blank=True)

        id_fme = models.TextField(db_column='id_fme', null=True, blank=True)
        fme_levels = models.DecimalField(db_column='fme_levels', max_digits=10, decimal_places=2, null=True, blank=True)
        fme_height = models.DecimalField(db_column='fme_height', max_digits=10, decimal_places=2, null=True, blank=True)

        h3_id = models.TextField(db_column='h3_id', null=True, blank=True)
        h3_res = models.SmallIntegerField(db_column='h3_res', null=True, blank=True)

        name = models.TextField(db_column='name', null=True, blank=True)

        class Meta:
            managed = False
            db_table = '"catalog"."houses"'
