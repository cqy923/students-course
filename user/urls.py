"""
作者：刘昱江
代码用途：
日期：2022 年 09 月 28 日
"""
from django.urls import path
from user import views


urlpatterns = [
    path('login/', views.home, name="login"),
    path('login/<slug:kind>', views.login, name="login"),
    path('register/<slug:kind>', views.register, name="register"),
    path('update/<slug:kind>', views.update, name="update"),
    path('logout/', views.logout, name="logout"),
]
