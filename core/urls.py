from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view # new
from drf_yasg import openapi


schema_view = get_schema_view( # new
    openapi.Info(
        title="University Counselling Center Api",
        default_version="v1",
        description="API for University Counselling Center",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hello@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),
    path('api/', include('self_help.urls')),
    path('api/counselors/', include('counselors.urls')),
    path('swagger/', schema_view.with_ui( # new
    'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui( # new
    'redoc', cache_timeout=0), name='schema-redoc'),
]
