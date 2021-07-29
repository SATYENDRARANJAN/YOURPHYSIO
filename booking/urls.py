from django.contrib import admin
from django.urls import path

import booking
from booking import views

urlpatterns = [
    path('',views.book_a_test)
]
