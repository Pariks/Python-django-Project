from django.shortcuts import render
from django.http import HttpResponse
from consulting.forms import ScheduleConsultationForm
from django.template.loader import render_to_string
from django.core.mail import send_mail

def index(request):
    if request.method == 'POST':
        form = ScheduleConsultationForm(request.POST)
        if form.is_valid():
            # Create, but don't save the new investor instance.
            info = form.save()
            msg_html = render_to_string('consulting/_email.html', {'info': info})
            send_mail('Request submitted', '', 'info@betoncombat.com', [info.email],  html_message=msg_html, fail_silently=True)
            form = ScheduleConsultationForm()
            c = {'form': form, 'consultation_var':1, 'req_sub':1}
            return render(request, 'consulting/index.html', c)
    else:
        form = ScheduleConsultationForm()
    if 'consultation' in request.GET or request.method == 'POST':
        consultation_var = 1
    else:                                                                                                                                  
        consultation_var = 0
    c = {'form': form, 'consultation_var':consultation_var}
    return render(request, 'consulting/index.html', c)

