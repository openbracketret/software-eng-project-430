from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Script(models.Model):
    """
    Model used to store scripts that are sent by other sources in order for better verification later on
    """

    created = models.DateField(auto_now=True)
    file = models.FileField(upload_to='script_files/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    max_redeems = models.IntegerField()

class Customer(models.Model):
    """
    Model used to store the information about customers
    """

    id_number = models.CharField(max_length=13)
    contact_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    address = models.CharField(max_length=256)

class ScriptRedeems(models.Model):
    """
    Model used to store when a customer redeems a script
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="script_redeems")
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="script_redeems")