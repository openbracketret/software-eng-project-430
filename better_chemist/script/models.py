from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Script(models.Model):
    """
    Model used to store scripts that are sent by other sources in order for better verification later on
    """

    
