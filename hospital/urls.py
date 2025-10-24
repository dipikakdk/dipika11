from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    # Queue System URLs
    
    path('generate-token/<int:patient_id>/', views.generate_token, name='generate_token'),
    path('queue/', views.queue_list, name='queue_list'),
    path('update-token/<int:token_id>/<str:new_status>/', views.update_token_status, name='update_token_status'),
    path('current-token/', views.current_token_view, name='current_token'),
]
