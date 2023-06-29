from django.urls import path
from .views import upload_deal, get_top_five_customers


urlpatterns = [
    path('upload_deal/', upload_deal),
    path('top_five_customers/', get_top_five_customers)
]
