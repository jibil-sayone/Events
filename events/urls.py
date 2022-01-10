from django.urls import path
from .views import index, updateEvent, createEvent, my_webhook_view, PublishEvent

urlpatterns = [
    path('', index, name='index'),
    path('create_task', createEvent, name="create_event"),
    path('update_task/<str:pk>/', updateEvent, name="update_event"),
    # path('payment/', CeatePaymentView.as_view(), name="pay"),
    path('payment/<str:pk>/', PublishEvent, name="pay"),
    path('webhook_stripe/', my_webhook_view, name="webhook-stripe")

]