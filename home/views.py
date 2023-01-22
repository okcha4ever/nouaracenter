from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from .models import Contact
from .forms import ContactForm
# Create your views here.

def home(request):
    return render(request, 'home.html')

def contact(request):
    submitted = False
    message1 = "! شكراً على تواصلكم معنا"
    message2 = "...سنرد في أقرب وقت ممكن"
    message3 = "! سنكون سعداء بمقابلتكم والاتصال بكم"
    message4 = "...الرجاء ملء الفراغات التالية"

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            message_name = form.cleaned_data['Full_Name']
            message = form.cleaned_data['Content']
            message_email = form.cleaned_data['Email']
            send_mail(
                f'From {message_name}/{message_email} ',
                message,
                settings.EMAIL_HOST_USER,
                ['minoukhiari4@gmail.com']
            )

        return HttpResponseRedirect('contact?submitted=True')
        
    else:
        form = ContactForm
        if 'submitted' in request.GET:
            submitted = True


    return render(request, 'contact.html', {'form': form, 'submitted': submitted, 'msg1': message1, 'msg2': message2, 'msg3': message3, 'msg4': message4})