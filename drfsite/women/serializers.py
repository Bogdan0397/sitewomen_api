from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women, Category, TagPost, Husband


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','id']

class HusbandSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Husband
        fields = ['name','id']
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = ['tag','slug']

class WomenSerializer(serializers.ModelSerializer):
    # users = serializers.HiddenField(default=serializers.CurrentUserDefault())
    categ = CatSerializer(read_only=True, source='cat')
    tagpost = TagSerializer(many=True,read_only=True, source='tags')
    class Meta:
        model = Women
        fields = ['id','tagpost','content','categ','title','slug','photo','time_create','time_update','is_published','cat','husband']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password','photo','id']



    # def create(self, validated_data):
    #     # Извлекаем пользователя из валидированных данных
    #     users = validated_data.pop('users', None)
    #
    #     # Создаем объект Women с оставшимися валидированными данными
    #     women_instance = Women.objects.create(**validated_data)
    #
    #     # Устанавливаем пользователя, если он был предоставлен
    #     if users:
    #         # Проверяем, является ли пользователь экземпляром модели User
    #         if isinstance(users, get_user_model()):
    #             women_instance.author = users
    #             women_instance.save()
    #         else:
    #             # Обрабатываем случай, если пользователь не является экземпляром User
    #             raise ValueError("Invalid users instance provided.")
    #     return women_instance
    #

