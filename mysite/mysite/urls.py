from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # включение URL-адресов приложения news
    # другие пути приложений, если они есть
]

# Добавление URL-адресов для django-debug-toolbar только в режиме DEBUG
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
