from django.db.models import Count
from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins, status
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import User
from .models import Women, Category, TagPost, Husband
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import WomenSerializer, CatSerializer, TagSerializer, HusbandSerialzier, UserSerializer


# class WomenAPIListPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'
#     max_page_size = 2


class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all().select_related('cat')
    serializer_class = WomenSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    # pagination_class = WomenAPIListPagination

class WomenPublishedAPIList(generics.ListAPIView):
    queryset = Women.objects.filter(is_published=True)
    serializer_class = WomenSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    # pagination_class = WomenAPIListPagination

class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, )


class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminOrReadOnly,)


class WomenAPIRetrieve(generics.RetrieveAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    lookup_field = 'slug'

class WomenCategoryAPIView(APIView):
    def get(self,request,slug):
        try:
            category = Category.objects.get(slug=slug)
            women_post = Women.objects.filter(cat=category)
            serializer = WomenSerializer(women_post, many=True)
            return Response(serializer.data)
        except:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


class WomenTagAPIView(APIView):
    def get(self,request,slug):
        try:
            tag = TagPost.objects.get(slug=slug)
            women_post = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
            serializer = WomenSerializer(women_post, many=True)
            return Response(serializer.data)
        except:
            return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)


class TagAPIList(generics.ListAPIView):
    queryset = TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)
    serializer_class = TagSerializer
    # pagination_class = WomenAPIListPagination


class CatAPIList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CatSerializer


class HusbandAPIList(generics.ListAPIView):
    queryset = Husband.objects.all()
    serializer_class = HusbandSerialzier


class UserAPIListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Извлекаем данные пользователя из запроса
        user_data = serializer.validated_data
        print(user_data)
        # Создаем пользователя, но не сохраняем его в базе данных
        user = User(**user_data)

        # Устанавливаем пароль с использованием метода set_password
        password = user_data.get('password')
        print('password')
        if password:
            user.set_password(password)

        # Сохраняем пользователя в базе данных
        user.save()

        # Продолжаем процесс создания пользователя, вызывая метод save() сериализатора
        serializer.save()

class UpdateRetrieveAPIUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Обновляем пароль, если он передан в запросе
        if 'password' in request.data:
            instance.set_password(request.data['password'])
            instance.save()
            return Response({'status': 'Password updated'}, status=status.HTTP_200_OK)

        # Продолжаем с обновлением остальных данных пользователя
        serializer.save()
        return Response(serializer.data)

class UpdateStrRetrieveAPIUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'