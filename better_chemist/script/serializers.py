from rest_framework import serializers

from script.models import Script


class ScriptBaseSerializer(serializers.ModelSerializer):
    """
    The base serializer for the Script model
    """


    class Meta:
        model = Script
        fields = '__all__'