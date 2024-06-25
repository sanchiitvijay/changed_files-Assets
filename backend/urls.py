"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from django.conf import settings
from asset_manager.api import urls as asset_urls
from security.api import urls as security_urls
from warehouse.api import urls as warehouse_urls
from tenant.api import urls as tenant_urls
from master.api import urls as master_urls
from purchase.api import urls as purchase_urls
from inventory.api import urls as inventory_urls
from asset_request.api import urls as asset_request_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Amigeo ERP",
        default_version='v1',
        description="Amigeo ERP",
        terms_of_service="https://www.sanaditechnologies.com",
        contact=openapi.Contact(email="info@sanaditechnologies.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  # <-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # <-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # <-- Here
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/tenant/', include(tenant_urls)),
    path('api/v1/<str:client>/security/', include(security_urls)),
    path('api/v1/<str:client>/asset/', include(asset_urls)),
    path('api/v1/<str:client>/warehouse/', include(warehouse_urls)),
    path('api/v1/<str:client>/master/', include(master_urls)),
    path('api/v1/<str:client>/purchase/', include(purchase_urls)),
    path('api/v1/<str:client>/inventory/', include(inventory_urls)),
    path('api/v1/<str:client>/asset-request/', include(asset_request_urls)),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.ASSET_ROOT}),
    # re_path(r'$.*', TemplateView.as_view(template_name="base.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.ASSET_URL, document_root=settings.ASSET_ROOT)
