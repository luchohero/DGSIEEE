from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^manage/$', 'app.views.index', name='index'),
    url(r'^manage/(\d+)/$', 'app.views.manage'),
    url(r'^$', 'app.views.ingresar'),
    url(r'^borrar/$', 'app.views.eliminar'),
    
    #url(r'^ieee/', include('ieee.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/$','app.views.nuevo'),
    url(r'^cerrar/$','app.views.cerrar'),

    url(r'^add/e/$','app.views.estado_f'),
    url(r'^(\d+)/$','app.views.perfil'),
    url(r'^add/u/$','app.views.usuario'),
    url(r'^add/us/$','app.views.usuario_names'),
    url(r'^agenda/','app.views.calendario'),
    url(r'^exportar/','app.views.exportar'),
    url(r'^manage/b/','app.views.buscar'),
    url(r'^suma/(\d+)/(\d+)/$','app.views.suma'),
)





