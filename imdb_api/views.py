from django.http import HttpResponse, JsonResponse
from django.http import Http404

from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from .models import Watchlist, StreamPlatform, Review
from .serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer

from rest_framework import mixins
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)


# entry point

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'watchlist': reverse('watch_list', request=request, format=format),
        'StreamPlatform': reverse('Streamplatform', request=request, format=format)
    })


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = Watchlist.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(review_user=review_user, watchlist=movie)
        if review_queryset:
            raise ValidationError("Cant review multiple times")
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2

            movie.number_rating += 1
            movie.save()
            serializer.save(watchlist=movie, review_user=review_user)


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class StreamPlatformViewSet(viewsets.ModelViewSet):
    """This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `delete` actions."""
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


# Using generic class-based views

# class StreamPlatformList(generics.ListCreateAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer
#
#
# class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer


# mixins

# class StreamPlatformList(mixins.ListModelMixin,
#                          mixins.CreateModelMixin,
#                          generics.GenericAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class StreamPlatformDetail(mixins.RetrieveModelMixin,
#                             mixins.UpdateModelMixin,
#                             mixins.DestroyModelMixin,
#                             generics.GenericAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# Api using class based views

# class StreamPlatformList(APIView):
#     """
#         List all StreamPlatformDetail, or create a new StreamPlatformDetail.
#         """
#
#     def get(self, request, format=None):
#         stream_list = StreamPlatform.objects.all()
#         serialized = StreamPlatformSerializer(stream_list, many=True)
#         return Response(serialized.data)
#
#     def post(self, request, format=None):
#         data = request.data
#         serialized = StreamPlatformSerializer(data=data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized, status=status.HTTP_201_CREATED)
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class StreamPlatformDetail(APIView):
#     """
#        Retrieve, update or delete a snippet instance.
#        """
#
#     def get_object(self, pk):
#         try:
#             stream_platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         stream_platform = self.get_object(pk)
#         serializer = StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         stream_platform = self.get_object(pk)
#         data = request.data
#         serializer = StreamPlatformSerializer(stream_platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk, format=None):
#         stream_platform = self.get_object(pk)
#         StreamPlatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
@api_view(['GET'])
def movie_list(request):
    movie_list = Watchlist.objects.all()
    serialized = WatchlistSerializer(movie_list, many=True)
    return Response(serialized.data, )


@api_view(['GET'])
def movie_detail(request, pk):
    movie = Watchlist.objects.get(pk=pk)
    serialized = WatchlistSerializer(movie)
    return Response(serialized.data)

# particular = get , put , delete
# lIST = get , post
# @api_view(['GET', 'POST'])
# def stream_list(request, format = None):
#     """
#         List all code StreamPlatform, or create a new StreamPlatform.
#         """
#     if request.method == 'GET':
#         stream_list = StreamPlatform.objects.all()
#         serialized = StreamPlatformSerializer(stream_list, many=True)
#         return Response(serialized.data, safe= False)
#
#     elif request.method == 'POST':
#         data = request.data
#         serialized = StreamPlatformSerializer(data = data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized, status = status.HTTP_201_CREATED)
#         return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)
#         # return JsonResponse(serialized.data, safe=False)


# @api_view(['GET', 'PUT', 'DELETE'])
# def stream_details(request, pk ,format = None):
#     """
#         Retrieve, update or delete a code snippet.
#         """
#     try:
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#     except StreamPlatform.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         data = request.data
#         serializer = StreamPlatformSerializer(stream_platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         StreamPlatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
