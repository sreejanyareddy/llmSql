from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name=''),
    path('generate_sql', views.generate_sql, name='index'),
    path('query_db',views.query_db,name= 'query_db')

    
]
