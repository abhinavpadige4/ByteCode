from django.contrib import admin
from django.urls import path
from chatbot.views import chatbot, login, register, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatbot/', chatbot, name='chatbot'),
    path('', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]
