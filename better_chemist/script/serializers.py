from rest_framework import serializers

from script.models import Script, Customer, ScriptRedeems


class ScriptBaseSerializer(serializers.ModelSerializer):
    """
    The base serializer for the Script model
    """


    class Meta:
        model = Script
        fields = '__all__'

class CustomerBaseSerializer(serializers.ModelSerializer):
    """
    The base serializer for the customer model
    """

    class Meta:
        model = Customer
        fields = '__all__'