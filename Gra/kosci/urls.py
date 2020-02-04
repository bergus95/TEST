from ..kosci import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.start),
    url(r'^wybor/$', views.wybor),
    url(r'^historia/$', views.historia),
    url(r'^ranking/$', views.ranking),
    url(r'^gracz1/$', views.gracz1),
    url(r'^gra/$', views.gra),
    url(r'^zajete/$', views.zajete),
    url(r'^koniec/$', views.koniec),
    url(r'^gracz2/$', views.gracz2)
]
