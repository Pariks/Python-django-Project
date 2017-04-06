from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from testimonial.models import TestimonialItem
from django.utils import timezone
from django.http import HttpResponseRedirect

def index(request):
    testimonialitems = TestimonialItem.objects.filter().order_by('order')

    c = {'testimonials':testimonialitems}

    return render(request, 'testimonial/index.html', c)
