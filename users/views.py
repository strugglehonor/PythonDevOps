from rest_framework.views import APIView
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from assets import models
from utils import Serializer, auth


# class User(ModelViewSet):
#     queryset = models.UserProfile.objects.all()
#     serializer_class = Serializer.UserSerializer
#     # authentication_classes = [auth, ]


class User(APIView):
    def get(self, request, *args, **kwargs):
        # 使用DRF的Response可以返回一个好看的页面，HTTPResponse没有这个效果
        return Response('GET OK')

    def post(self, request, *args, **kwargs):
        print(request.data)
        return HttpResponse('POST OK')
