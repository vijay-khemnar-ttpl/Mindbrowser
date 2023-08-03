from rest_framework import serializers
from .models import Alert, Asset, Rule
from authentication.serializers import UserSerializer


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):

    asset = AssetSerializer(many=True,read_only=True)
    
    class Meta:
        model = Alert
        fields = ['alert_type', 'value', 'alert_condition', 'asset', 'message']


