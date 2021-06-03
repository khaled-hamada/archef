from django.urls import path
from archef import views



app_name = 'archef'


urlpatterns = [
    path('start_page/', views.start_page , name='start_page'),
    path('search/', views.search , name='search'),
    path('view/', views.view_results, name='view'),
    path('store/', views.store, name='store'),
    path('edit/<int:record_id>/', views.edit, name='edit'),
    path('edit_d/<int:decision_id>/', views.edit_d, name='edit_d'),
    path('edit_redirect/<int:decision_id>/', views.edit_redirect, name='edit_redirect'),
    path('delete/<int:record_id>/', views.delete, name='delete'),
]
