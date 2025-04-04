from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_spectacular import views as rest_views

urlpatterns = [
    path(
        'v1/faces/',
        include('scores.api.urls')
    ),
    path(
        'api/schema/',
        rest_views.SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'api/schema/swagger-ui/',
        rest_views.SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        rest_views.SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
    path(
        'admin/',
        admin.site.urls
    )
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
