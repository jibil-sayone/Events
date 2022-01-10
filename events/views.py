from django.shortcuts import render,redirect
from django.http import HttpResponse
import django.views.generic
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *
import stripe
# Create your views here.

stripe.api_key = 'sk_test_51KGQMoSHH8WqtIRyo6XGgOPRlC0HO7G8lvnFAb1CtPymhUjUOrCGDUSiDqCw5dZValm5FeOyduM0KAsXyVkqy27C00B4S7SURw'
endpoint_secret = "whsec_jgZliM2H6ycKmBzvttqVgNr3USAsFXpA"
YOUR_DOMAIN = 'http://localhost:8020'

def index(request):
	tasks = Event.objects.all()

	form = EventForm()
	context = {'tasks':tasks, 'form':form}
	return render(request, 'events/list.html', context)


def updateEvent(request, pk):
	task = Event.objects.get(id=pk)

	form = EventForm(instance=task)

	if request.method == 'POST':
		form = EventForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'task':task,'form':form}

	return render(request, 'events/update_event.html', context)

def createEvent(request):

	form = EventForm()

	if request.method =='POST':
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')

	context = {'form':form}

	return render(request, 'events/create_event.html', context)


def PublishEvent(request, pk):
	checkout_session = stripe.checkout.Session.create(
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Events',
				},
				'unit_amount': 2000,
			},
			'quantity': 1,
		}],
	mode='payment',
	success_url=YOUR_DOMAIN + '',
	cancel_url=YOUR_DOMAIN + '',
	)
	event = Event.objects.get(id=pk)
	event.paid = True
	event.published = True
	event.save()
	return redirect(checkout_session.url, code=303)


@csrf_exempt
def my_webhook_view(request):
	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None

	try:
		event = stripe.Webhook.construct_event(
		  payload, sig_header, endpoint_secret
		)
	except ValueError as e:
		# Invalid payload
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		return HttpResponse(status=400)

	if event["type"] == 'checkout.session.completed':
		session = event["data"]["object"]

		if session.payment_status == 'paid':

			fullfill_order()

	return HttpResponse(status=200)

def fullfill_order():
	pass