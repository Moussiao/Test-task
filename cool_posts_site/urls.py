import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from cool_posts_site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('my_clients.urls')),
    path('', include('strange_posts.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
