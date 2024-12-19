from rest_framework import serializers
from api.models import UserBonuses, BonusLevel
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BonusLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusLevel
        fields = '__all__'


class UserBonusesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = BonusLevelSerializer()

    class Meta:
        model = UserBonuses
        fields = ['user', 'current_spending', 'level']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BonusProgramSerializer(serializers.Serializer):
    current_level = serializers.CharField()
    cashback_percentage = serializers.IntegerField()
    next_level = serializers.CharField()
    next_level_threshold = serializers.IntegerField()
    current_spending = serializers.IntegerField()
