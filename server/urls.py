from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def list_routes(request):
    """Debug view to list all available URLs"""
    from django.urls.resolvers import get_resolver
    resolver = get_resolver()
    urls = []
    
    def list_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                list_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                urls.append({
                    'url': prefix + str(pattern.pattern),
                    'name': getattr(pattern, 'name', None),
                    'callback': str(pattern.callback.__qualname__ if hasattr(pattern, 'callback') else '')
                })
    
    list_urls(resolver.url_patterns)
    return JsonResponse({'urls': urls})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('__debug__/urls/', list_routes),  # Debug URL
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)