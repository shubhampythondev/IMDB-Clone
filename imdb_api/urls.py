from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'stream', views.StreamPlatformViewSet, basename="streamplatform")

urlpatterns = [
    path('list/', views.movie_list, name="watch-list"),
    path('list/<int:pk>', views.movie_detail, name='watchlist-detail'),
    path('list/<int:pk>/review/', views.ReviewListView.as_view(), name='review-list'),
    path('list/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    # path('list/review/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('', include(router.urls)),
    path('', views.api_root),
]
# urlpatterns = format_suffix_patterns(urlpatterns)


# streamplatform_List = views.StreamPlatformViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# streamplatform_detail = views.StreamPlatformViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
