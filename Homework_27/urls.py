from django.contrib import admin
from django.urls import path

from my_apps import views
from my_apps.views import CategoriesView, AdsView, CategoryDetailView, AdsDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.first_step),
    path('ads/', views.second_step),
    path('categories/', views.csv_to_json),
    path('cat/', CategoriesView.as_view()),
    path('ad/', AdsView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('ad/<int:pk>/', AdsDetailView.as_view()),
]
