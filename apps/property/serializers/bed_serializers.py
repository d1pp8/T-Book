from rest_framework import serializers
from apps.property.models import Bed


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = [
            'uuid',
            'bed_type',
            'quantity'
        ]
        read_only_fields = ['uuid']

class ChoiceSerializer(serializers.Serializer):
    value = serializers.CharField(help_text="Internal value.")
    label = serializers.CharField(help_text="Human-readable label.")