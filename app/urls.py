from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('register', views.register,name='register'),
    path('show', views.show,name='show'),
    path('attendance', views.attendance,name='attendance'),
    path('register/face',views.registerface,name='registerface'),
    path("register/successfully",views.registerface,name="user_added")
]