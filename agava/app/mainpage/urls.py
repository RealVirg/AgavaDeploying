from django.urls import path
from . import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('doc/', views.doc, name='doc'),
    path('login/', views.user_login, name='user_login'),
    path('doc/<int:id>', views.doc_detail, name="doc_detail"),
    path('reg/', views.reg, name='reg'),
    path('logout/', views.user_logout, name='user_logout')
]
