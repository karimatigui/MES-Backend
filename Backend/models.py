from django.db import models

class IonAPICredentials(models.Model):
    ti = models.CharField(max_length=100)
    cn = models.CharField(max_length=50)
    dt = models.CharField(max_length=10)
    ci = models.TextField()
    cs = models.TextField()
    iu = models.URLField()
    pu = models.URLField()
    oa = models.CharField(max_length=100)
    ot = models.CharField(max_length=100)
    or_field = models.CharField(max_length=100, db_column='or')  # 'or' is a Python keyword
    sc = models.JSONField(default=list)  # Assuming it's always a list
    ev = models.CharField(max_length=50)
    v = models.CharField(max_length=10)
    company = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"IonAPI for {self.cn} ({self.ti})"
# ---------------------------------------------------------------

class UserAccount(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # hashed password
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)  # this updates every time the record is saved
    def __str__(self):
        return self.username
