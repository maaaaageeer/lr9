from decimal import Decimal

from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.authentication import generate_jwt_token
from api.models import UserBonuses, BonusLevel
from api.permissions import IsAuthenticated
from api.serializers import LoginSerializer, BonusProgramSerializer


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            token = generate_jwt_token(user.id, user.username)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Неправильный логин или пароль"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_level_data(spending):
    levels = BonusLevel.objects.order_by('spending_threshold')
    current_level = None
    next_level = None
    next_level_threshold = None

    for level in levels:
        if spending >= level.spending_threshold:
            current_level = level

        else:
            if next_level is None:
                next_level = level
                next_level_threshold = int(next_level.spending_threshold)

    if not current_level:
        current_level = BonusLevel.objects.filter(spending_threshold__exact=0).first()
        if not current_level:
            raise exceptions.NotFound("Не найден начальный уровень")
    if not next_level:
        next_level = current_level
        next_level_threshold = int(next_level.spending_threshold)

    return current_level, next_level, next_level_threshold


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bonus_view(request):
    user = request.user
    try:
        user_bonus = UserBonuses.objects.get(user=user)
        current_level, next_level, next_level_threshold = get_level_data(user_bonus.current_spending)
        data = {
            "current_level": current_level.level_name,
            "cashback_percentage": current_level.cashback_percentage,
            "next_level": next_level.level_name,
            "next_level_threshold": next_level_threshold,
            "current_spending": int(user_bonus.current_spending)
        }
    except UserBonuses.DoesNotExist:
        current_level, next_level, next_level_threshold = get_level_data(Decimal(0))
        data = {
            "current_level": current_level.level_name,
            "cashback_percentage": current_level.cashback_percentage,
            "next_level": next_level.level_name,
            "next_level_threshold": next_level_threshold,
            "current_spending": 0
        }

    serializer = BonusProgramSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)