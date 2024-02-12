from django.urls import path
from Demo import views

urlpatterns = [
    path('', views.home, name='start'),
    path('formToken', views.formToken, name='formToken'),
    path('result', views.paidResult, name='result'),
    path('ipn', views.ipn, name='ipn')
]