from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from leases import views



from . import views

app_name = 'leases'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'upload/$', views.upload, name='upload'),
    url(r'bulk/$', views.bulk, name='bulk'),
    url(r'approved/$', views.approved, name='approved'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
