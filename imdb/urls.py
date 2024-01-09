from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('imdb_api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path("swagger-ui/", TemplateView.as_view(template_name="swagger-ui.html",
                                             extra_context={"schema_url": "openapi-schema"}, ),
         name="swagger-ui", ),
path('openapi', get_schema_view(
            title="IMDB Clone",
            description="IMDB API  is a compact Django Rest Framework project designed to provide "
                        "comprehensive information about movies, including their details, reviews,"
                        " and integration with streaming platforms. ",
            version="1.0.0"
        ), name='openapi-schema'),
]
