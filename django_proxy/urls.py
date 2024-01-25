from django.urls import path
from .views import user_authentication, user_cabinet, change_attribute, proxy_view, create_site


urlpatterns = [
    path('', user_authentication, name='user_authentication'),
    path('user_cabinet/', user_cabinet, name='user_cabinet'),
    path('change_attribute/', change_attribute, name='change_attribute'),
    path('proxy/', proxy_view, name='proxy_view'),
    path('proxy/<path:url>', proxy_view, name='proxy_view_url'),
    path('create_site/', create_site, name='create_site'),
]
