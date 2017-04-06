from django.conf import settings

def stripekey(request):
    return { 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY }