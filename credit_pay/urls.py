from django.urls import path
from . import views
urlpatterns = [
    path('create_charge/', views.create_charge),
    path('capture_charge/<charge_id>', views.capture_charge),
    path('create_refund/<charge_id>', views.create_refund),
    path('get_charges/', views.get_charges),
]

# 1. Create charge for credit card payment
# 1. POST /api/v1/create_charge
# 2. Capture the created charge
# 1. POST /api/v1/capture_charge/:chargeId
# 3. Create a refund for the created charge
# 1. POST /api/v1/create_refund/:chargeId
# 4. Get a List of all charges
# 1. GET /api/v1/get_charges